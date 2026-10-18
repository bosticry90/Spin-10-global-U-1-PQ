# Replay controller path correction V2

Primary scientific worker completed. The first replay controller stopped before
launch because an inherited predecessor path requested primary_v2_capture.json;
the actual primary capture is primary_capture.json. No replay scientific worker
ran and no physics result is inferred. Preserve original controller/source/
preparation and its prelaunch failure record. Corrected controller uses the
actual complete primary receipt,authenticates the unchanged original preparation
and source,and runs only replay. Same120-second/8GiB limits and all math checks.
