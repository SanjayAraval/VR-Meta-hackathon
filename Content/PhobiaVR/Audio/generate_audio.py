import os
import wave
import math
import struct
import random

audio_dir = r"c:\Users\sanja\OneDrive\Desktop\meta 3d\Content\PhobiaVR\Audio"
os.makedirs(audio_dir, exist_ok=True)

def write_wav(filename, samples, sample_rate=44100):
    filepath = os.path.join(audio_dir, filename)
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)  # Mono for 3D spatialization in UE5
        wf.setsampwidth(2)   # 16-bit
        wf.setframerate(sample_rate)
        # Convert float samples (-1.0 to 1.0) to 16-bit PCM
        packed_frames = bytearray()
        for s in samples:
            val = max(-1.0, min(1.0, s))
            int_val = int(val * 32767)
            packed_frames.extend(struct.pack('<h', int_val))
        wf.writeframes(packed_frames)
    print(f"Generated {filepath} ({len(samples)/sample_rate:.2f}s)")

sample_rate = 44100

# 1. Calm Zen Meditation Chime (Safe Room / Decompression Lifeline)
def generate_zen_chime():
    duration = 4.0
    num_samples = int(duration * sample_rate)
    samples = []
    base_freq = 528.0  # Solfeggio "love / transformation" frequency
    harmonics = [(1.0, 1.0), (2.0, 0.4), (3.0, 0.2), (4.2, 0.1)]
    for i in range(num_samples):
        t = i / sample_rate
        # Slow exponential decay
        envelope = math.exp(-t * 0.9) * (1.0 - math.exp(-t * 20.0))
        val = 0.0
        for mult, amp in harmonics:
            val += math.sin(2 * math.pi * base_freq * mult * t) * amp
        samples.append(val * envelope * 0.6)
    write_wav("A_ZenChime_Safe.wav", samples)

# 2. Skyscraper High Altitude Wind Gusts (Acrophobia)
def generate_wind_loop():
    duration = 6.0
    num_samples = int(duration * sample_rate)
    samples = []
    # Band-limited noise with slow howling resonant modulation
    noise_buf = [random.uniform(-1.0, 1.0) for _ in range(num_samples)]
    # Simple lowpass filter
    filtered = 0.0
    for i in range(num_samples):
        t = i / sample_rate
        # Modulating cutoff frequency between 300Hz and 900Hz
        howl_lfo = 0.5 + 0.5 * math.sin(2 * math.pi * 0.25 * t) + 0.2 * math.sin(2 * math.pi * 0.7 * t)
        alpha = 0.03 + 0.06 * howl_lfo
        filtered = filtered + alpha * (noise_buf[i] - filtered)
        # Whistling overtone
        whistle = math.sin(2 * math.pi * (450 + 150 * math.sin(2 * math.pi * 0.3 * t)) * t) * 0.15 * howl_lfo
        samples.append((filtered * 0.7 + whistle) * 0.5)
    write_wav("A_Wind_HighAltitude_Loop.wav", samples)

# 3. Elevator Mechanical Motor & Cable Groan (Claustrophobia)
def generate_elevator_cable_groan():
    duration = 5.0
    num_samples = int(duration * sample_rate)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        # Low mechanical rumble (45Hz + 90Hz)
        rumble = (math.sin(2 * math.pi * 48 * t) * 0.5 + 
                  math.sin(2 * math.pi * 96 * t) * 0.3 + 
                  math.sin(2 * math.pi * 144 * t) * 0.15)
        # Metal cable friction / creak burst around t = 2.0s
        creak_env = math.exp(-((t - 2.2) ** 2) / 0.15)
        creak_freq = 620 + 200 * math.sin(2 * math.pi * 8 * t)
        metal_creak = math.sin(2 * math.pi * creak_freq * t) * creak_env * 0.5
        samples.append((rumble * 0.4 + metal_creak) * 0.7)
    write_wav("A_Elevator_Stall_Groan.wav", samples)

# 4. Spooky Spider Scuttle / Click Sounds (Arachnophobia)
def generate_spider_skitter():
    duration = 2.0
    num_samples = int(duration * sample_rate)
    samples = [0.0] * num_samples
    # Random short sharp clicks mimicking chitinous spider feet tapping
    random.seed(42)
    step_times = [random.uniform(0.1, 1.9) for _ in range(24)]
    step_times.sort()
    for st in step_times:
        start_idx = int(st * sample_rate)
        click_dur = int(0.015 * sample_rate)  # 15ms click
        freq = random.uniform(1800, 3200)
        for j in range(click_dur):
            idx = start_idx + j
            if idx < num_samples:
                ct = j / sample_rate
                env = math.exp(-ct * 350.0)
                click = math.sin(2 * math.pi * freq * ct) * env * random.uniform(0.3, 0.7)
                samples[idx] += click
    write_wav("A_Spider_Skitter_Cue.wav", samples)

# 5. Audience Ambient Murmur (Glossophobia)
def generate_audience_murmur():
    duration = 6.0
    num_samples = int(duration * sample_rate)
    samples = []
    # Layered filtered pseudo-formants mimicking distant crowd chatter & quiet room reflections
    f1 = 280.0
    f2 = 720.0
    f3 = 1400.0
    noise_buf = [random.uniform(-1.0, 1.0) for _ in range(num_samples)]
    s1, s2 = 0.0, 0.0
    for i in range(num_samples):
        t = i / sample_rate
        lfo1 = math.sin(2 * math.pi * 0.15 * t)
        lfo2 = math.cos(2 * math.pi * 0.35 * t)
        s1 += 0.05 * (noise_buf[i] - s1)
        # Subtle human vowel-like formants
        voice_sim = (math.sin(2 * math.pi * f1 * t) * (0.2 + 0.1 * lfo1) +
                     math.sin(2 * math.pi * f2 * t) * (0.15 + 0.08 * lfo2) +
                     math.sin(2 * math.pi * f3 * t) * 0.08)
        # Occasional quiet cough or page shuffle at t=3.5
        cough_env = math.exp(-((t - 3.5) ** 2) / 0.05)
        cough = (random.uniform(-0.4, 0.4)) * cough_env
        samples.append((s1 * 0.3 + voice_sim * 0.15 + cough) * 0.4)
    write_wav("A_Audience_Murmur_Loop.wav", samples)

# 6. Biometric Heartbeat Pulse (Wrist Watch / Biofeedback)
def generate_heartbeat():
    duration = 2.0  # 60-80 BPM simulated cycle
    num_samples = int(duration * sample_rate)
    samples = [0.0] * num_samples
    # Two beat pulses: Lub (t=0.1) and Dub (t=0.45)
    beats = [(0.1, 55.0, 0.8, 0.08), (0.42, 70.0, 0.6, 0.06)]
    for beat_time, freq, amp, decay_time in beats:
        start_idx = int(beat_time * sample_rate)
        dur_samples = int(0.25 * sample_rate)
        for j in range(dur_samples):
            idx = start_idx + j
            if idx < num_samples:
                bt = j / sample_rate
                env = math.exp(-bt / decay_time) * math.sin(math.pi * min(1.0, bt / 0.02))
                val = math.sin(2 * math.pi * freq * bt) * env * amp
                samples[idx] += val
    write_wav("A_Heartbeat_Pulse_Cue.wav", samples)

if __name__ == "__main__":
    generate_zen_chime()
    generate_wind_loop()
    generate_elevator_cable_groan()
    generate_spider_skitter()
    generate_audience_murmur()
    generate_heartbeat()
    print("All spatial audio cues successfully synthesized.")
