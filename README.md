# Directional Acoustic Gesture Control Using Laptop Microphones

## 1. Project Overview

**Directional Acoustic Gesture Control** is a human-computer interaction system that uses the built-in microphone array of a laptop to detect table-tapping sounds and determine whether the tap originated from the **left, center, or right** side of the laptop.

The detected direction and tap pattern are then converted into configurable computer commands such as taking a screenshot, opening Gmail, controlling media, opening applications, or executing other operating-system actions.

The core idea is to treat a table tap as an **acoustic gesture** rather than using a physical input device.

---

## 2. Problem Statement

Traditional computer interaction relies heavily on keyboards, mice, touchpads, and touchscreens. This project explores an alternative interaction method in which a user can perform simple table-tapping gestures near a laptop and have the computer interpret them as commands.

The challenge is to:

1. Capture audio from the laptop's microphone array.
2. Detect whether a tap occurred.
3. Determine the direction from which the tap reached the laptop.
4. Distinguish between single, double, and multiple taps.
5. Convert the detected gesture into a user-configurable computer action.
6. Reject background sounds and uncertain detections.

---

## 3. Main Objective

The main objective is to develop a real-time system that can:

```text
Table Tap
    ↓
Audio Capture
    ↓
Tap Detection
    ↓
Direction Estimation
    ↓
Gesture Recognition
    ↓
Command Mapping
    ↓
Computer Action
```

Example:

```text
Left-side tap  → Take Screenshot
Right-side tap → Open Gmail
Center tap     → Open Browser
Double tap     → Play/Pause
```

The mappings should be configurable rather than permanently hard-coded.

---

## 4. Core Concept

A laptop with multiple microphones can capture the same acoustic event through different microphone channels.

For a tap closer to the left microphone:

```text
Tap
 |
 +----> Left microphone  : earlier / stronger
 |
 +----> Right microphone : later / weaker
```

For a tap closer to the right microphone:

```text
Tap
 |
 +----> Left microphone  : later / weaker
 |
 +----> Right microphone : earlier / stronger
```

The system can use these differences to estimate the tap direction.

The primary measurements are:

- **Time Difference of Arrival (TDOA)**
- **Amplitude/Energy Difference**
- **Cross-correlation between microphone signals**

---

# 5. System Architecture

```text
                    ┌─────────────────────────┐
                    │      Physical World     │
                    │                         │
                    │   User taps the table   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Audio Acquisition   │
                    │                         │
                    │  Left Mic + Right Mic   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Signal Preprocessing  │
                    │                         │
                    │ Noise Reduction         │
                    │ Filtering               │
                    │ Normalization           │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      Tap Detection      │
                    │                         │
                    │ Energy / Peak Detection │
                    │ Transient Detection     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Direction Estimation  │
                    │                         │
                    │ TDOA                    │
                    │ Amplitude Difference    │
                    │ Cross-Correlation       │
                    └────────────┬────────────┘
                                 │
                         LEFT / RIGHT / CENTER
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Gesture Recognition   │
                    │                         │
                    │ Single Tap              │
                    │ Double Tap              │
                    │ Multiple Tap            │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Command Mapping       │
                    │                         │
                    │ Gesture → Action        │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     OS Controller       │
                    │                         │
                    │ Screenshot              │
                    │ Applications            │
                    │ Browser / Gmail         │
                    │ Media Controls          │
                    └─────────────────────────┘
```

---

# 6. Detailed Architecture

## 6.1 Audio Acquisition

The audio acquisition module continuously receives audio from the laptop's microphone system.

### Requirements

- Microphone input
- Preferably two independent microphone channels
- Real-time audio streaming
- Sufficient sampling rate for transient detection

The system should preserve the separate microphone channels.

> **Important:** Do not convert stereo microphone input to mono before direction estimation because this can remove the spatial information required to determine left/right direction.

---

## 6.2 Signal Preprocessing

Raw microphone input can contain:
- Fan noise
- Keyboard noise
- Speech
- Music
- Air-conditioning noise
- Environmental sounds
- Electrical noise
The preprocessing module prepares the signal for tap detection.

### Processing pipeline

```text
Raw Audio
    ↓
Noise Reduction
    ↓
Band-pass Filtering
    ↓
Normalization
    ↓
Processed Audio
```

Possible Python tools:

- NumPy
- SciPy
- SoundDevice

---

## 6.3 Tap Detection

The tap detector determines whether the incoming sound contains a table-tap event.

A simple initial implementation can use:

- Short-time energy
- RMS energy
- Peak amplitude
- Threshold detection
- Transient duration

Example:

```text
Background:

______________________________

Tap:

___________________/\__________
                   ↑
               Threshold
```

When a short acoustic event exceeds the required threshold, the system marks it as a possible tap.

---

## 6.4 Direction Estimation

Direction estimation is the core component of the project.

### Time Difference of Arrival

Let:

```text
tL = arrival time at left microphone
tR = arrival time at right microphone
```

Then:

```text
Δt = tR - tL
```

Conceptually:

```text
If tL < tR
    → sound reached left microphone first
    → likely LEFT

If tR < tL
    → sound reached right microphone first
    → likely RIGHT

If |tL - tR| is very small
    → likely CENTER
```

The actual thresholds should be determined experimentally during calibration.

---

## 6.5 Amplitude Difference

Arrival time should not be the only measurement because laptop microphone spacing is small and the timing difference may be very small.

The system can also compare signal amplitudes.

```text
ΔA = AL - AR
```

Where:

- `AL` = amplitude/energy measured by the left microphone
- `AR` = amplitude/energy measured by the right microphone

Example:

```text
LEFT tap:

Left microphone  = high
Right microphone = lower
```

and:

```text
RIGHT tap:

Left microphone  = lower
Right microphone = high
```

---

## 6.6 Cross-Correlation

Cross-correlation can be used to estimate the relative delay between the two microphone signals.

```text
Left Signal  ─────┐
                  │
                  ├── Cross Correlation ──> Estimated Delay
                  │
Right Signal ─────┘
```

This can be more robust than detecting the peak independently in both channels.

---

# 7. Direction Classifier

The system can initially use a rule-based classifier.

Conceptually:

```text
                 Tap Detected
                      │
              Extract Features
                      │
          ┌───────────┴───────────┐
          │                       │
        Δt                      ΔA
          │                       │
          └───────────┬───────────┘
                      │
               Direction Model
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        LEFT        CENTER       RIGHT
```

A future version can replace the rule-based classifier with machine learning.

### Possible ML models

- Support Vector Machine
- Random Forest
- Logistic Regression
- Small Neural Network

---

# 8. Gesture Recognition

Direction can be combined with the number and timing of taps.

A gesture can be represented as:

```text
Gesture = {
    direction,
    tap_count,
    timing,
    confidence
}
```

Example:

```text
{
    direction: LEFT,
    tap_count: 1,
    confidence: 0.91
}
```

Possible gestures:

| Gesture | Meaning |
|---|---|
| Left + single tap | Left command |
| Right + single tap | Right command |
| Center + single tap | Center command |
| Left + double tap | Custom command |
| Right + double tap | Custom command |
| Triple tap | Custom command |

---

# 9. Gesture State Machine

The gesture engine can use a state machine to avoid interpreting random noises as commands.

```text
                 ┌──────────────┐
                 │     IDLE     │
                 └──────┬───────┘
                        │
                  Sound detected
                        │
                        ▼
              ┌───────────────────┐
              │  POSSIBLE TAP     │
              └─────────┬─────────┘
                        │
                 Tap validation
                        │
                ┌───────┴───────┐
                │               │
              Valid           Invalid
                │               │
                ▼               ▼
          TAP DETECTED         IDLE
                │
                ▼
       WAIT FOR NEXT TAP
                │
         ┌──────┴──────┐
         │             │
       Timeout       Another tap
         │             │
         ▼             ▼
    Single Tap     Double Tap
```

This allows the system to distinguish different tap patterns.

---

# 10. Command Mapping

The command mapping layer separates gesture recognition from actual computer actions.

Instead of hard-coding commands:

```text
LEFT = Screenshot
RIGHT = Gmail
```

the system should use a configurable mapping:

```text
Gesture
   ↓
Command Mapper
   ↓
Configured Action
```

Example configuration:

```text
LEFT_SINGLE_TAP   → SCREENSHOT
RIGHT_SINGLE_TAP  → OPEN_GMAIL
CENTER_SINGLE_TAP → OPEN_BROWSER
LEFT_DOUBLE_TAP   → PREVIOUS_TRACK
RIGHT_DOUBLE_TAP  → NEXT_TRACK
CENTER_DOUBLE_TAP → PLAY_PAUSE
```

This makes the system extensible.

---

# 11. Operating System Controller

The OS controller executes the selected command.

Possible actions include:

- Take screenshot
- Open Gmail
- Open a browser
- Launch an application
- Play/pause media
- Next/previous track
- Increase/decrease volume
- Switch windows
- Lock the computer
- Execute a custom command

The exact implementation depends on the operating system.

---

# 12. Calibration System

Different laptops have different:

- Microphone positions
- Microphone sensitivity
- Microphone spacing
- Audio drivers
- Acoustic characteristics

Therefore, a calibration module should be included.

### Calibration procedure

The user performs multiple taps at:

```text
LEFT
CENTER
RIGHT
```

The system records samples and calculates typical:

```text
Time difference
Amplitude difference
Signal energy
Noise level
```

The results are used to determine suitable thresholds.

### Calibration flow

```text
Start Calibration
       ↓
Record Background Noise
       ↓
Record Left Taps
       ↓
Record Center Taps
       ↓
Record Right Taps
       ↓
Calculate Features
       ↓
Calculate Thresholds
       ↓
Save Calibration Data
```

---

# 13. Confidence and Noise Rejection

Not every detected sound should trigger a command.

The system should calculate a confidence value based on factors such as:

- Tap strength
- Timing difference
- Amplitude difference
- Correlation quality
- Similarity to calibrated tap samples

Example:

```text
Confidence > threshold
        ↓
Execute command

Confidence < threshold
        ↓
Ignore event
```

This helps prevent false commands caused by speech, keyboard sounds, or other environmental noise.

---

# 14. Recommended Technology Stack

## Programming Language

**Python**

## Audio Processing

- `sounddevice`
- `numpy`
- `scipy`
- `librosa` (optional)

## Machine Learning

- `scikit-learn`
- PyTorch/TensorFlow (optional advanced implementation)

## GUI

- Tkinter for a simple interface
- PySide/PyQt for a more advanced interface

## OS Automation

Depending on the target operating system:

- `pyautogui`
- `subprocess`
- OS-specific APIs

---

# 15. Suggested Software Architecture

```text
project/
│
├── main.py
│
├── audio/
│   ├── audio_manager.py
│   ├── microphone.py
│   └── buffer.py
│
├── signal_processing/
│   ├── filters.py
│   ├── noise_reduction.py
│   ├── normalization.py
│   └── features.py
│
├── detection/
│   ├── tap_detector.py
│   ├── direction_estimator.py
│   └── confidence.py
│
├── gesture/
│   ├── gesture_recognizer.py
│   └── state_machine.py
│
├── commands/
│   ├── command_mapper.py
│   ├── os_controller.py
│   └── actions.py
│
├── calibration/
│   ├── calibration.py
│   └── thresholds.py
│
├── ui/
│   ├── main_window.py
│   └── settings.py
│
├── config/
│   └── gestures.json
│
├── data/
│   ├── calibration/
│   └── samples/
│
├── models/
│   └── direction_model.pkl
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# 16. Example Configuration

A `gestures.json` file could contain:

```json
{
    "LEFT_SINGLE_TAP": "SCREENSHOT",
    "RIGHT_SINGLE_TAP": "OPEN_GMAIL",
    "CENTER_SINGLE_TAP": "OPEN_BROWSER",
    "LEFT_DOUBLE_TAP": "PREVIOUS_TRACK",
    "RIGHT_DOUBLE_TAP": "NEXT_TRACK",
    "CENTER_DOUBLE_TAP": "PLAY_PAUSE"
}
```

---

# 17. End-to-End Data Flow

```text
                 TABLE TAP
                     │
                     ▼
            LAPTOP MICROPHONES
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
     LEFT CHANNEL          RIGHT CHANNEL
          │                     │
          └──────────┬──────────┘
                     ▼
               AUDIO BUFFER
                     │
                     ▼
             PREPROCESSING
                     │
                     ▼
               TAP DETECTOR
                     │
                Tap found?
                /          \
              NO            YES
              │              │
              │              ▼
              │       FEATURE EXTRACTION
              │              │
              │        ┌─────┴─────┐
              │        ▼           ▼
              │       ΔT           ΔA
              │        │           │
              │        └─────┬─────┘
              │              ▼
              │      DIRECTION ESTIMATOR
              │              │
              │       LEFT/CENTER/RIGHT
              │              │
              │              ▼
              │      GESTURE RECOGNIZER
              │              │
              │       SINGLE/DOUBLE/etc.
              │              │
              │              ▼
              │       COMMAND MAPPER
              │              │
              │              ▼
              │        OS CONTROLLER
              │              │
              │              ▼
              │       COMPUTER ACTION
              │
              └──────► CONTINUE LISTENING
```

---

# 18. Development Roadmap

## Phase 1 — Microphone Testing

Verify that the laptop exposes the required microphone channels.

Goals:

- Detect available audio devices
- Identify channel count
- Record left/right channels
- Plot or inspect recorded signals

### Important checkpoint

If the laptop only exposes processed mono audio, the original two-channel direction-estimation approach may not work as intended.

---

## Phase 2 — Tap Detection

Implement:

- Audio buffering
- Energy calculation
- Peak detection
- Tap threshold
- Noise rejection

Output:

```text
TAP DETECTED
```

---

## Phase 3 — Direction Detection

Implement:

- TDOA estimation
- Amplitude comparison
- Cross-correlation
- Direction thresholds

Output:

```text
LEFT
CENTER
RIGHT
```

---

## Phase 4 — Gesture Recognition

Add:

- Single tap
- Double tap
- Triple tap
- Tap timing
- Gesture state machine

---

## Phase 5 — Computer Commands

Connect gestures to:

- Screenshot
- Gmail
- Browser
- Media controls
- Applications

---

## Phase 6 — Calibration

Implement:

- Background-noise calibration
- Left/right/center tap collection
- Automatic threshold calculation
- Calibration storage

---

## Phase 7 — Machine Learning

Collect labelled samples:

```text
LEFT
CENTER
RIGHT
```

Extract features and train a classifier.

Possible pipeline:

```text
Audio
  ↓
Preprocessing
  ↓
Feature Extraction
  ↓
Feature Vector
  ↓
ML Classifier
  ↓
LEFT / CENTER / RIGHT
```

---

# 19. Testing Strategy

The system should be tested under different conditions.

## Direction Tests

Test taps:

- Close to left side
- Center of laptop
- Close to right side
- Different distances
- Different tap strengths

## Noise Tests

Test while:

- Fan is running
- Keyboard is being used
- People are talking
- Music is playing
- Background noise is present

## Gesture Tests

Test:

- Single tap
- Double tap
- Triple tap
- Fast taps
- Slow taps

## Performance Metrics

Useful metrics include:

### Direction accuracy

```text
Direction Accuracy =
Correct Direction Predictions / Total Valid Taps
```

### Tap detection accuracy

Measure:

- True positives
- False positives
- False negatives

### Command latency

Measure the time between:

```text
Physical Tap
      ↓
Command Execution
```

---

# 20. Potential Challenges

### 1. Microphone limitations

Laptop microphones may be very close together, making timing differences difficult to measure.

### 2. Audio processing by drivers

Some systems may apply:

- Noise suppression
- Echo cancellation
- Beamforming
- Automatic gain control

These can modify the raw microphone signals.

### 3. Background noise

Other sounds may resemble taps.

### 4. Table characteristics

Different tables can change:

- Sound propagation
- Resonance
- Tap intensity
- Frequency response

### 5. User position

The same physical tap can produce different signals depending on where the laptop and user are positioned.

Calibration helps address these differences.

---

# 21. Future Enhancements

Possible future improvements include:

- Full 2D tap localization
- More than two microphones
- Machine-learning-based gesture recognition
- Personalized user profiles
- Adaptive noise cancellation
- Voice + tap hybrid commands
- Custom gesture creation
- Mobile-device support
- Smart-home control
- Accessibility applications
- Real-time visualization of detected direction

With more microphones, the system could potentially move from:

```text
LEFT / CENTER / RIGHT
```

toward:

```text
2D POSITION ESTIMATION
```

---

# 22. Security and Safety Considerations

Because the system can execute operating-system commands, actions should be configurable and potentially protected by confidence thresholds.

For sensitive operations, consider requiring:

```text
Gesture
+
High confidence
+
Optional confirmation
```

The application should also avoid executing arbitrary commands from untrusted configuration files.

---

# 23. Expected Final System

The completed system should operate approximately as follows:

```text
User taps table
       ↓
Laptop microphones capture sound
       ↓
System detects acoustic transient
       ↓
System compares microphone signals
       ↓
Direction is estimated
       ↓
Tap pattern is recognized
       ↓
Gesture is mapped to a command
       ↓
Computer executes the command
       ↓
System returns to listening mode
```

Example:

```text
        User taps left side
                 ↓
        Audio captured
                 ↓
          Tap detected
                 ↓
        Direction = LEFT
                 ↓
       Gesture = SINGLE TAP
                 ↓
        Command = SCREENSHOT
                 ↓
        Screenshot captured
```

---

# 24. Project Summary

**Directional Acoustic Gesture Control Using Laptop Microphones** is a real-time human-computer interaction project that transforms ordinary table taps into computer commands.

The system combines:

- Digital signal processing
- Audio acquisition
- Microphone-array processing
- Time Difference of Arrival
- Amplitude analysis
- Cross-correlation
- Gesture recognition
- Optional machine learning
- Operating-system automation

The architecture is intentionally modular so that the audio-processing system, direction estimator, gesture recognizer, and command system can be developed and tested independently.

The first implementation should focus on reliably achieving:

```text
Tap Detection
      +
LEFT / CENTER / RIGHT Detection
      +
Single / Double Tap Recognition
      +
Configurable Computer Actions
```

Once these components work reliably, machine learning and more advanced gesture recognition can be added as an enhancement.
