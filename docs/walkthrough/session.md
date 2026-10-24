# Session walkthrough

`HostSession` sends a `TIME_SYNC` frame at connection setup. Every valid request receives an `ACK` followed by the action response. Successful project open/simulation responses also emit `PROJECT_EVENT`, allowing the device's NVS context history to learn completed work. The session itself does not bypass the allow-list or confirmation gate.

The time-sync epoch is current host time and the offset is the host's local UTC offset. Cross-device clock accuracy still requires measured PING round-trip data and is not claimed here.
