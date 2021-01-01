# Medical Ultrasound
Wave reconstruction raytracing for medical transcranial ultrasound.
## Howto
WARNING. Project not finished yet.
There are 4 steps:
1. Computing physics. Run main.cpp in src. This step takes about 1 hour. It generates files in data.
2. Processing of computed data. Use 2_hilbertize.py. It generates spectra of signals for each sensor.
3. Building single data file from 32 sensors. Use 3_focus.cpp (this file is not in every branch).
4. Assembling the final image. Use 4_sectorize.py
The result is in data
