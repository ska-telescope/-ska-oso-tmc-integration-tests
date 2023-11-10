Given the TMC is on.

Given the TMC Subarray is in one of the <obsState>
|Examples|
|obsState|
|IDLE|
|READY|
|SCANNING|
|CONFIGURING|

When the Abort command is invoked on TMC Subarray.

Then the TMC Subarray transitions to ABORTING state.

And after completion, TMC Subarray transitions to ABORTED state.

When the Restart command is invoked on TMC Subarray.

Then the TMC Subarray transitions to RESTARTING state.

And after completion, TMC Subarray transitions to EMPTY state.