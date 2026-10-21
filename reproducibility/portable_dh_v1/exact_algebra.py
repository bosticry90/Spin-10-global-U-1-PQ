"""Finite exact graded algebra for the one complete DH reproduction pilot.

Coefficient cells are (xi power, eta_H power, radical mask).  The fixed
radical squares are (2, 3, 5, 7, -1).  This is not a general QFT compiler.
"""
import ast
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json

SQUARES = (2, 3, 5, 7, -1)
ONE = (((0, 0, 0), Fraction(1)),)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add_coefficients(left, right):
    if not left:
        return right
    if not right:
        return left
    result = dict(left)
    for cell, value in right:
        result[cell] = result.get(cell, Fraction(0)) + value
    return tuple((cell, value) for cell, value in sorted(result.items()) if value)


def scale_coefficient(value, factor):
    if factor == 1:
        return value
    return tuple((cell, number * factor) for cell, number in value if number * factor)


@lru_cache(maxsize=131072)
def multiply_coefficients(left, right):
    result = {}
    for (xi, eta, mask), a in left:
        for (xi2, eta2, mask2), b in right:
            factor = a * b
            for bit, square in enumerate(SQUARES):
                if mask & mask2 & (1 << bit):
                    factor *= square
            cell = xi + xi2, eta + eta2, mask ^ mask2
            result[cell] = result.get(cell, Fraction(0)) + factor
    return tuple((cell, value) for cell, value in sorted(result.items()) if value)


def expression_add(left, right):
    result = dict(left)
    for key, value in right.items():
        result[key] = result.get(key, Fraction(0)) + value
        if not result[key]:
            del result[key]
    return result


def expression_product(left, right):
    result = {}
    for (g, xi, eta, mask), a in left.items():
        for (g2, xi2, eta2, mask2), b in right.items():
            coefficient = multiply_coefficients(
                (((xi, eta, mask), a),), (((xi2, eta2, mask2), b),)
            )
            for (xx, hh, mm), value in coefficient:
                key = g + g2, xx, hh, mm
                result[key] = result.get(key, Fraction(0)) + value
                if not result[key]:
                    del result[key]
    return result


def inverse_constant(expression):
    require(len(expression) == 1, "denominator must be one nonzero exact constant")
    (g, xi, eta, mask), value = next(iter(expression.items()))
    require(g == xi == eta == 0 and value != 0, "variable denominator forbidden")
    square = 1
    for bit, prime in enumerate(SQUARES):
        if mask & (1 << bit):
            square *= prime
    return {(0, 0, 0, mask): 1 / (value * square)}


def rational_square_root(value):
    require(value >= 0, "negative square root must use explicit I")

    def integer_root(number):
        outside, mask = 1, 0
        for bit, prime in enumerate(SQUARES[:4]):
            exponent = 0
            while number and number % prime == 0:
                number //= prime
                exponent += 1
            outside *= prime ** (exponent // 2)
            if exponent % 2:
                mask |= 1 << bit
        require(number == 1, "unsupported radical prime")
        return {(0, 0, 0, mask): Fraction(outside)}

    if value == 0:
        return {}
    return expression_product(integer_root(value.numerator), inverse_constant(integer_root(value.denominator)))


@lru_cache(maxsize=16384)
def parse_coefficient(text):
    """Parse a restricted exact expression; never eval arbitrary source text."""
    symbols = {
        "g10": {(1, 0, 0, 0): Fraction(1)},
        "xi": {(0, 1, 0, 0): Fraction(1)},
        "reference_width_M": {(0, 1, 0, 0): Fraction(1)},
        "eta_H": {(0, 0, 1, 0): Fraction(1)},
        "reference_width_H": {(0, 0, 1, 0): Fraction(1)},
        "I": {(0, 0, 0, 16): Fraction(1)},
    }

    def evaluate(node):
        if isinstance(node, ast.Constant):
            require(type(node.value) is int, "floating or noninteger literal forbidden")
            return {(0, 0, 0, 0): Fraction(node.value)} if node.value else {}
        if isinstance(node, ast.Name):
            require(node.id in symbols, "unknown coefficient symbol: " + node.id)
            return symbols[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            sign = -1 if isinstance(node.op, ast.USub) else 1
            return {key: sign * value for key, value in evaluate(node.operand).items()}
        if isinstance(node, ast.BinOp):
            left, right = evaluate(node.left), evaluate(node.right)
            if isinstance(node.op, ast.Add):
                return expression_add(left, right)
            if isinstance(node.op, ast.Sub):
                return expression_add(left, {key: -value for key, value in right.items()})
            if isinstance(node.op, ast.Mult):
                return expression_product(left, right)
            if isinstance(node.op, ast.Div):
                return expression_product(left, inverse_constant(right))
            if isinstance(node.op, ast.Pow):
                power = right.get((0, 0, 0, 0), Fraction(0))
                require(set(right) <= {(0, 0, 0, 0)} and power.denominator == 1 and abs(power) <= 8, "invalid power")
                if power < 0:
                    left = inverse_constant(left)
                result = {(0, 0, 0, 0): Fraction(1)}
                for _ in range(abs(int(power))):
                    result = expression_product(result, left)
                return result
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            require(node.func.id == "sqrt" and len(node.args) == 1 and not node.keywords, "unsupported function")
            argument = evaluate(node.args[0])
            require(set(argument) <= {(0, 0, 0, 0)}, "root of a variable forbidden")
            return rational_square_root(argument.get((0, 0, 0, 0), Fraction(0)))
        raise ValueError("unsupported exact coefficient expression")

    grouped = {}
    for (g, xi, eta, mask), value in evaluate(ast.parse(text, mode="eval").body).items():
        require(g >= 0 and xi >= 0 and eta >= 0 and 0 <= mask < 32, "invalid coefficient cell")
        grouped[g] = add_coefficients(grouped.get(g, ()), (((xi, eta, mask), value),))
    return tuple(sorted(grouped.items()))


def put(polynomial, key, coefficient):
    if coefficient:
        value = add_coefficients(polynomial.get(key, ()), coefficient)
        if value:
            polynomial[key] = value
        else:
            polynomial.pop(key, None)


def combine(*polynomials):
    result = {}
    for polynomial in polynomials:
        for key, value in polynomial.items():
            put(result, key, value)
    return result


def scale(polynomial, factor):
    return {key: scale_coefficient(value, factor) for key, value in polynomial.items()} if factor else {}


class Algebra:
    def __init__(self, names, parities):
        require(len(names) == len(set(names)) == len(parities), "invalid alphabet")
        require(all(type(p) is int and p in (0, 1) for p in parities), "invalid field parity")
        self.names = tuple(names)
        self.parities = tuple(parities)
        self.index = {name: i for i, name in enumerate(names)}

    def token(self, text):
        name, _, suffix = text.partition("__")
        require(name in self.index and all(mu in "0123" for mu in suffix), "unknown field or jet")
        jets = tuple(map(int, suffix))
        require(jets == tuple(sorted(jets)), "noncanonical derivative order")
        return self.index[name], jets

    @lru_cache(maxsize=262144)
    def canonical(self, word):
        odd = [token for token in word if self.parities[token[0]]]
        if len(set(odd)) != len(odd):
            return (), 0
        inversions = sum(a > b for i, a in enumerate(odd) for b in odd[i + 1:])
        return tuple(sorted(word)), -1 if inversions % 2 else 1

    def rows(self, rows, explicit_g=False):
        result = {}
        for row in rows:
            word = tuple(self.token(name) for name in row["word"])
            require(self.canonical(word) == (word, 1), "noncanonical input word")
            terms = parse_coefficient(row["coefficient"])
            if explicit_g:
                require(type(row["g"]) is int and row["g"] >= 0, "invalid explicit g order")
                require(all(g == 0 for g, value in terms), "g counted twice")
            for g, value in terms:
                put(result, (row["g"] if explicit_g else g, word), value)
        return result

    def action(self, polynomial, replacements, method="slot", wrong_odd=False):
        result = {}
        for (g, word), value in polynomial.items():
            prefix_parity = 0
            for position, (field, jets) in enumerate(word):
                if field in replacements:
                    replacement = replacements[field]
                    require(self.parities[field] == self.parities[replacement], "operation must be even")
                    token = (replacement, jets)
                    rest = word[:position] + word[position + 1:]
                    if method == "slot":
                        key, sign = self.canonical(word[:position] + (token,) + word[position + 1:])
                        if wrong_odd:
                            sign *= (-1) ** prefix_parity
                    else:
                        require(method == "left", "unknown derivative method")
                        key, sign = self.canonical((token,) + rest)
                        sign *= (-1) ** (self.parities[field] * prefix_parity)
                    if sign:
                        put(result, (g, key), scale_coefficient(value, sign))
                prefix_parity += self.parities[field]
        return result

    def product(self, left, right):
        result = {}
        for (g, word), value in left.items():
            for (g2, word2), value2 in right.items():
                key, sign = self.canonical(word + word2)
                if sign:
                    put(result, (g + g2, key), scale_coefficient(multiply_coefficients(value, value2), sign))
        return result

    def fingerprint(self, polynomial):
        digest = sha256()
        digest.update(b"[")
        for i, ((g, word), value) in enumerate(sorted(polynomial.items())):
            if i:
                digest.update(b",")
            row = [g, [[self.names[n], list(j)] for n, j in word], [[list(cell), str(number)] for cell, number in value]]
            digest.update(json.dumps(row, separators=(",", ":"), ensure_ascii=True).encode())
        digest.update(b"]")
        return digest.hexdigest()

    def decode_compact(self, packet):
        require(packet["schema"] == "FINITE_EXACT_COMPONENT_INTERNED_CELLS_V1", "unsupported packet")
        require(packet["alphabet"] == list(self.names) and packet["basis_squared"] == list(SQUARES), "basis mismatch")
        coefficients = []
        for rows in packet["coefficients"]:
            require(bool(rows) and rows == sorted(rows, key=lambda row: row[:3]), "invalid coefficient order")
            seen = set()
            value = []
            for xi, eta, mask, numerator, denominator in rows:
                require(all(type(z) is int for z in (xi, eta, mask, numerator, denominator)), "noninteger cell")
                require(xi >= 0 and eta >= 0 and 0 <= mask < 32 and numerator != 0 and denominator > 0, "invalid cell")
                cell = xi, eta, mask
                require(cell not in seen, "duplicate coefficient cell")
                seen.add(cell)
                fraction = Fraction(numerator, denominator)
                require((fraction.numerator, fraction.denominator) == (numerator, denominator), "unnormalized rational")
                value.append((cell, fraction))
            coefficients.append(tuple(value))
        result, used = {}, set()
        for g, tokens, coefficient_id in packet["monomials"]:
            require(type(g) is int and g >= 0, "invalid coupling order")
            require(type(coefficient_id) is int and 0 <= coefficient_id < len(coefficients), "invalid coefficient index")
            require(all(type(n) is int and 0 <= n < len(self.names) for n, jets in tokens), "invalid field index")
            require(all(jets == sorted(jets) and all(type(mu) is int and 0 <= mu < 4 for mu in jets) for n, jets in tokens), "invalid jets")
            word = tuple((n, tuple(jets)) for n, jets in tokens)
            require(self.canonical(word) == (word, 1) and (g, word) not in result, "invalid or duplicate monomial")
            result[g, word] = coefficients[coefficient_id]
            used.add(coefficient_id)
        require(used == set(range(len(coefficients))), "unused coefficient")
        require(self.fingerprint(result) == packet["sha256_exact_cells"], "compact coefficient hash mismatch")
        return result
