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

# 1. Dark Psychological Horror Drone (Deep Tritone & Binaural Dread)
def generate_horror_drone():
    duration = 8.0
    num_samples = int(duration * sample_rate)
    samples = []
    # Dissonant tritone: Root 55Hz (A1) and Tritone 77.78Hz (Eb2)
    # Plus binaural beat: 40Hz and 46Hz (6Hz Theta anxiety wave)
    for i in range(num_samples):
        t = i / sample_rate
        lfo = 0.5 + 0.5 * math.sin(2 * math.pi * 0.18 * t)
        lfo_fast = math.sin(2 * math.pi * 1.5 * t)
        
        # Sub-bass rumblings
        sub = math.sin(2 * math.pi * 38 * t) * 0.4 + math.sin(2 * math.pi * 44 * t) * 0.3
        
        # Discordant tritone cluster
        tritone = (math.sin(2 * math.pi * 55 * t) * 0.35 + 
                   math.sin(2 * math.pi * 77.78 * t) * 0.3 + 
                   math.sin(2 * math.pi * 110 * t) * 0.15)
        
        # Ghostly eerie glass chime resonance (wavering pitch)
        eerie_freq = 880 + 35 * math.sin(2 * math.pi * 0.4 * t)
        ghost_lead = math.sin(2 * math.pi * eerie_freq * t) * 0.12 * lfo
        
        # Low mechanical pulse / rhythmic dread thud
        pulse = math.sin(2 * math.pi * 65 * t) * max(0.0, math.sin(2 * math.pi * 0.75 * t)) ** 4 * 0.35
        
        mix = (sub * 0.5 + tritone * 0.4 + ghost_lead + pulse * 0.3) * 0.85
        samples.append(mix)
    write_wav("A_Horror_Drone_Ominous.wav", samples)

# 2. Piercing Jumpscare / Stinger (Microtonal Cluster Shriek & Sub-Impact)
def generate_jumpscare_stinger():
    duration = 3.2
    num_samples = int(duration * sample_rate)
    samples = [0.0] * num_samples
    # Massive initial explosive impact at t=0.05
    for i in range(num_samples):
        t = i / sample_rate
        if t < 0.02:
            continue
        st = t - 0.02
        # Initial explosive sub drop (boom)
        boom_env = math.exp(-st * 4.0)
        boom = math.sin(2 * math.pi * (160 * math.exp(-st * 8.0) + 30) * st) * boom_env * 0.8
        
        # Razor-sharp microtonal violin cluster shriek (Penderecki style)
        shriek_env = math.exp(-st * 2.2) * (1.0 - math.exp(-st * 150.0))
        cluster = 0.0
        # 10 tightly spaced high frequencies (dissonant clash)
        frequencies = [1240, 1285, 1310, 1370, 1420, 1490, 1560, 1610, 1720, 1850]
        for f in frequencies:
            # Add frequency modulation (tremolo / terror screech)
            fm = f + 40 * math.sin(2 * math.pi * 14.0 * st)
            cluster += math.sin(2 * math.pi * fm * st)
        cluster = (cluster / len(frequencies)) * shriek_env * 0.85
        
        # Harsh noise transient
        noise_env = math.exp(-st * 18.0)
        noise = random.uniform(-0.6, 0.6) * noise_env
        
        samples[i] = boom * 0.7 + cluster * 0.75 + noise * 0.35
    write_wav("A_Jumpscare_Violin_Shriek.wav", samples)

# 3. Violent Elevator Cable Snap & Metallic Drop (Claustrophobia Terror)
def generate_cable_snap_drop():
    duration = 5.0
    num_samples = int(duration * sample_rate)
    samples = [0.0] * num_samples
    
    # 0.0 - 1.2s: Extreme groaning cable tension under load
    # 1.2s: Sharp metallic ping and catastrophic violent cable SNAP!
    # 1.25 - 3.5s: Freefall rushing wind, squealing emergency brakes, heavy iron impacts
    for i in range(num_samples):
        t = i / sample_rate
        if t < 1.2:
            # Creaking steel tension
            tension_freq = 420 + 200 * (t / 1.2) ** 2
            groan = math.sin(2 * math.pi * tension_freq * t) * (0.3 + 0.4 * (t / 1.2))
            rumble = math.sin(2 * math.pi * 50 * t) * 0.3
            samples[i] = (groan + rumble) * 0.5
        elif t >= 1.2 and t < 1.4:
            # The SNAP (whip crack + metallic ping)
            st = t - 1.2
            snap_env = math.exp(-st * 80.0)
            ping_env = math.exp(-st * 12.0)
            snap = random.uniform(-1.0, 1.0) * snap_env
            ping = math.sin(2 * math.pi * 2800 * st) * ping_env * 0.8
            samples[i] = snap * 0.9 + ping * 0.7
        else:
            # Plummet and scraping metal brakes
            st = t - 1.4
            drop_env = math.exp(-st * 0.8)
            # Screeching metal on metal (FM brake squeal)
            brake_fm = 1800 + 600 * math.sin(2 * math.pi * 45 * st)
            brake_squeal = math.sin(2 * math.pi * brake_fm * st) * drop_env * 0.4
            # Heavy cabin shuddering impact at st = 1.0 (t = 2.4s)
            impact_st = st - 1.0
            impact = 0.0
            if impact_st > 0:
                imp_env = math.exp(-impact_st * 6.0)
                impact = (math.sin(2 * math.pi * 60 * impact_st) * 0.7 + 
                          random.uniform(-0.5, 0.5)) * imp_env * 0.8
            # Low rushing wind
            wind = random.uniform(-0.25, 0.25) * drop_env
            samples[i] = brake_squeal * 0.5 + impact * 0.8 + wind * 0.3
    write_wav("A_Cable_Snap_Crash.wav", samples)

# 4. Horrifying Chitinous Spider Swarm & Hissing (Arachnophobia)
def generate_spider_swarm_frenzy():
    duration = 4.0
    num_samples = int(duration * sample_rate)
    samples = [0.0] * num_samples
    
    # Over 80 sharp, crisp, wet clicks and rapid scurrying feet
    random.seed(666)
    num_clicks = 120
    click_times = [random.uniform(0.1, 3.8) for _ in range(num_clicks)]
    click_times.sort()
    
    for ct in click_times:
        start_idx = int(ct * sample_rate)
        dur = int(random.uniform(0.008, 0.025) * sample_rate)
        freq = random.uniform(2200, 4800)
        amp = random.uniform(0.3, 0.8)
        for j in range(dur):
            idx = start_idx + j
            if idx < num_samples:
                t_j = j / sample_rate
                env = math.exp(-t_j * 400.0)
                click = math.sin(2 * math.pi * freq * t_j) * env * amp
                samples[idx] += click
                
    # Add aggressive, venomous wet insect hissing
    for i in range(num_samples):
        t = i / sample_rate
        # Hiss envelope swells between 1.0s and 3.0s
        hiss_env = max(0.0, math.sin(2 * math.pi * 0.35 * t)) ** 2
        # Bandpassed noise for snake/spider venom hiss
        hiss = random.uniform(-0.4, 0.4) * hiss_env * 0.35
        # Low eerie insect flutter
        flutter = math.sin(2 * math.pi * (25 + 10 * math.sin(2 * math.pi * 8 * t)) * t) * 0.15
        samples[i] += hiss + flutter
        
    write_wav("A_Spider_Swarm_Frenzy.wav", samples)

# 5. Terrifying Vertigo Abyss Wind & Shepard Falling Tone (Acrophobia)
def generate_vertigo_abyss():
    duration = 6.0
    num_samples = int(duration * sample_rate)
    samples = []
    
    # Shepard descending scale (the psychological illusion of falling forever)
    # Mixed with brutal howling high-altitude gusts
    for i in range(num_samples):
        t = i / sample_rate
        # Desolately howling gale-force wind
        wind_gust = 0.5 + 0.5 * math.sin(2 * math.pi * 0.4 * t)
        noise = random.uniform(-1.0, 1.0)
        
        # Modulating resonant pitch filter (whistle)
        whistle_pitch = 500 + 350 * math.sin(2 * math.pi * 0.6 * t + 0.5)
        whistle = math.sin(2 * math.pi * whistle_pitch * t) * 0.25 * wind_gust
        
        # Descending void frequencies (endless fall sensation)
        desc1 = math.sin(2 * math.pi * (220 - 20 * (t % 2.0)) * t) * 0.15
        desc2 = math.sin(2 * math.pi * (110 - 10 * (t % 2.0)) * t) * 0.2
        desc3 = math.sin(2 * math.pi * (55 - 5 * (t % 2.0)) * t) * 0.3
        
        mix = (noise * 0.35 * wind_gust + whistle + desc1 + desc2 + desc3) * 0.75
        samples.append(mix)
    write_wav("A_Vertigo_Abyss_Wind.wav", samples)

# 6. Eerie Paranoid Whispers & Judging Murmurs (Glossophobia / Psychological Dread)
def generate_creepy_whispers():
    duration = 6.0
    num_samples = int(duration * sample_rate)
    samples = [0.0] * num_samples
    
    # Layered speech-like vowel formants modulated with eerie whispering noise
    formants = [(320, 0.3), (780, 0.25), (1250, 0.2), (2400, 0.15), (3200, 0.1)]
    for i in range(num_samples):
        t = i / sample_rate
        lfo_pan = math.sin(2 * math.pi * 0.5 * t)
        lfo_rate = 0.3 + 0.2 * math.sin(2 * math.pi * 0.2 * t)
        
        voice_cluster = 0.0
        for f, weight in formants:
            # Modulate formant to simulate shifting whispered speech ("pssst... they see you...")
            mod_f = f + 45 * math.sin(2 * math.pi * lfo_rate * 4 * t)
            voice_cluster += math.sin(2 * math.pi * mod_f * t) * weight
            
        whisper_noise = random.uniform(-0.3, 0.3) * (0.4 + 0.3 * math.sin(2 * math.pi * 1.2 * t))
        
        # Reverse swell stinger at t = 4.5s
        swell = 0.0
        if 3.8 < t < 4.8:
            st = (t - 3.8) / 1.0
            swell = (st ** 3) * math.sin(2 * math.pi * 660 * t) * 0.4
            
        samples[i] = (voice_cluster * 0.35 + whisper_noise * 0.5 + swell) * 0.7
    write_wav("A_Whispers_Paranoia_Loop.wav", samples)

# 7. Extreme Tachycardia Panic Heartbeat & Choking Breath
def generate_panic_heartbeat_breath():
    duration = 4.0
    num_samples = int(duration * sample_rate)
    samples = [0.0] * num_samples
    
    # Severe Tachycardia: 150 BPM pulse (every 0.4s)
    bpm_interval = 0.4
    num_beats = int(duration / bpm_interval)
    for b in range(num_beats):
        bt = b * bpm_interval
        # Lub
        start1 = int(bt * sample_rate)
        for j in range(int(0.08 * sample_rate)):
            idx = start1 + j
            if idx < num_samples:
                tj = j / sample_rate
                samples[idx] += math.sin(2 * math.pi * 65 * tj) * math.exp(-tj * 45.0) * 0.9
        # Dub
        start2 = int((bt + 0.12) * sample_rate)
        for j in range(int(0.07 * sample_rate)):
            idx = start2 + j
            if idx < num_samples:
                tj = j / sample_rate
                samples[idx] += math.sin(2 * math.pi * 85 * tj) * math.exp(-tj * 55.0) * 0.7
                
    # Suffocation / Hyperventilating ragged breath in the background
    for i in range(num_samples):
        t = i / sample_rate
        # Inhale (1.0s), exhale (0.8s) rapid cycle
        cycle = t % 1.2
        breath_env = math.exp(-((cycle - 0.3) ** 2) / 0.03) + math.exp(-((cycle - 0.8) ** 2) / 0.02)
        breath = random.uniform(-0.35, 0.35) * breath_env * 0.5
        samples[i] += breath
        
    write_wav("A_Tachycardia_Suffocation.wav", samples)

if __name__ == "__main__":
    print("Synthesizing terrifying eerie horror audio suite...")
    generate_horror_drone()
    generate_jumpscare_stinger()
    generate_cable_snap_drop()
    generate_spider_swarm_frenzy()
    generate_vertigo_abyss()
    generate_creepy_whispers()
    generate_panic_heartbeat_breath()
    print("All 7 eerie horror soundscapes synthesized successfully.")
