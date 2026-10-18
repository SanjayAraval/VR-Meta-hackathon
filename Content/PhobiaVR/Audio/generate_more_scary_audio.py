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
        wf.setnchannels(1)  # Mono for 3D HRTF spatialization in OpenXR
        wf.setsampwidth(2)   # 16-bit
        wf.setframerate(sample_rate)
        packed_frames = bytearray()
        for s in samples:
            val = max(-1.0, min(1.0, s))
            int_val = int(val * 32767)
            packed_frames.extend(struct.pack('<h', int_val))
        wf.writeframes(packed_frames)
    print(f"Generated {filepath} ({len(samples)/sample_rate:.2f}s, {len(samples)} samples)")

sample_rate = 44100

# 1. Thalassophobia: Deep Ocean Abyss (Hydrostatic pressure, distant sub sonar, monstrous low groan)
def generate_thalassophobia_abyss():
    duration = 8.0
    num_samples = int(duration * sample_rate)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        # Deep crushing underwater pressure rumble (30Hz + 60Hz)
        water_rumble = (math.sin(2 * math.pi * 32 * t) * 0.5 + 
                        math.sin(2 * math.pi * 64 * t) * 0.3)
        # Deep underwater bubble gurgle
        bubble_lfo = math.sin(2 * math.pi * 0.3 * t)
        bubble = math.sin(2 * math.pi * (140 + 40 * math.sin(2 * math.pi * 6 * t)) * t) * 0.15 * max(0.0, bubble_lfo)
        # Eerie distant sonar ping at t=2.0 and t=6.0
        sonar = 0.0
        for ping_time in [2.0, 6.0]:
            if ping_time <= t < ping_time + 1.2:
                st = t - ping_time
                sonar += math.sin(2 * math.pi * 820 * st) * math.exp(-st * 3.5) * 0.4
        # Guttural deep sea leviathan groan at t=4.0
        leviathan = 0.0
        if 3.5 < t < 5.5:
            st = t - 3.5
            env = math.sin(math.pi * (st / 2.0)) ** 2
            leviathan = math.sin(2 * math.pi * (45 + 15 * math.sin(2 * math.pi * 1.5 * st)) * st) * env * 0.6
        mix = (water_rumble * 0.6 + bubble + sonar + leviathan) * 0.85
        samples.append(mix)
    write_wav("A_Thalassophobia_Abyss_Sonar.wav", samples)

# 2. Nyctophobia / Achluophobia: Absolute Darkness (Scratching on walls, frantic lighter clicks, breath behind you)
def generate_nyctophobia_darkness():
    duration = 6.0
    num_samples = int(duration * sample_rate)
    samples = [0.0] * num_samples
    for i in range(num_samples):
        t = i / sample_rate
        # Deep claustrophobic sensory deprivation silence with high-frequency tinnitus whine (8000Hz faint)
        tinnitus = math.sin(2 * math.pi * 7800 * t) * 0.04
        # Low ominous air current
        air = (random.uniform(-0.15, 0.15)) * (0.5 + 0.5 * math.sin(2 * math.pi * 0.25 * t))
        samples[i] = tinnitus + air
    # Add frantic failed lighter strikes at t=1.0, 1.8, 2.5
    for strike in [1.0, 1.8, 2.5]:
        start = int(strike * sample_rate)
        dur = int(0.06 * sample_rate)
        for j in range(dur):
            if start + j < num_samples:
                tj = j / sample_rate
                samples[start + j] += random.uniform(-0.8, 0.8) * math.exp(-tj * 70.0)
    # Creepy dry fingernails scratching against drywall at t=3.5 to 5.0
    scratch_start = int(3.5 * sample_rate)
    scratch_dur = int(1.5 * sample_rate)
    for j in range(scratch_dur):
        idx = scratch_start + j
        if idx < num_samples:
            tj = j / sample_rate
            scratch_mod = math.sin(2 * math.pi * 22 * tj)
            scratch = random.uniform(-0.4, 0.4) * max(0.0, scratch_mod) * 0.6
            samples[idx] += scratch
    write_wav("A_Nyctophobia_Whispering_Dark.wav", samples)

# 3. Automatonophobia / Coulrophobia: Creepy Living Dolls & Distorted Music Box
def generate_automaton_music_box():
    duration = 7.0
    num_samples = int(duration * sample_rate)
    samples = []
    # Eerie, detuned music box melody in minor key: E5, G5, B5, C6, B5, G5, Eb5
    notes = [659.25, 783.99, 987.77, 1046.50, 987.77, 783.99, 622.25]
    note_dur = 0.9
    for i in range(num_samples):
        t = i / sample_rate
        note_idx = int(t / note_dur) % len(notes)
        note_t = t % note_dur
        freq = notes[note_idx]
        # Detuned double tone (eerie warble)
        mb_env = math.exp(-note_t * 3.0)
        box_tone = (math.sin(2 * math.pi * freq * note_t) * 0.6 + 
                    math.sin(2 * math.pi * (freq * 1.015) * note_t) * 0.4) * mb_env
        # Wooden joint creak bursts at note transitions
        creak = 0.0
        if note_t < 0.08:
            creak = random.uniform(-0.5, 0.5) * math.exp(-note_t * 60.0)
        # Low drone underneath
        drone = math.sin(2 * math.pi * 110 * t) * 0.2
        samples.append((box_tone * 0.55 + creak * 0.3 + drone) * 0.8)
    write_wav("A_Automaton_MusicBox_Creep.wav", samples)

# 4. Megalophobia / Astrophobia: Colossal Seismic Titan Monolith Drone
def generate_megalophobia_titan():
    duration = 8.0
    num_samples = int(duration * sample_rate)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        # Seismic infrasound rumble (24Hz + 36Hz + 48Hz)
        infra = (math.sin(2 * math.pi * 24 * t) * 0.5 + 
                 math.sin(2 * math.pi * 36 * t) * 0.35 + 
                 math.sin(2 * math.pi * 48 * t) * 0.2)
        # Giant cosmic cavernous wind
        hollow_wind = (random.uniform(-0.3, 0.3)) * (0.6 + 0.4 * math.sin(2 * math.pi * 0.15 * t))
        # Deep metallic resonant hum of immense monolithic structure
        monolith = math.sin(2 * math.pi * (72 + 8 * math.sin(2 * math.pi * 0.2 * t)) * t) * 0.3
        mix = (infra * 0.65 + hollow_wind * 0.4 + monolith * 0.35) * 0.9
        samples.append(mix)
    write_wav("A_Megalophobia_Titan_Drone.wav", samples)

if __name__ == "__main__":
    print("Synthesizing expanded horror audio suite for comprehensive phobia matrix...")
    generate_thalassophobia_abyss()
    generate_nyctophobia_darkness()
    generate_automaton_music_box()
    generate_megalophobia_titan()
    print("All additional horror tracks synthesized successfully.")
