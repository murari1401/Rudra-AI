import pvporcupine as pv
import pyaudio
import struct
import os

ACCESS_KEY = "qT9JGhJ1dYaEUopKIIxNM7IrLoCFNd+6xSp4yrWbNgRf7Jtiyk5JaQ=="

def start_listening(callback):
    keyword_path = os.path.join(os.path.dirname(__file__), "hey-rudra_en_windows_v3_0_0.ppn")

    porcupine = pv.create(
        access_key=ACCESS_KEY,
        keyword_paths=[keyword_path]
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("🟢 Waiting for wake word...")

    try:
        while True:
            data = stream.read(porcupine.frame_length, exception_on_overflow=False)
            samples = struct.unpack_from("h" * porcupine.frame_length, data)
            result = porcupine.process(samples)
            if result >= 0:
                print("🔊 Wake word detected!")
                callback()
    except KeyboardInterrupt:
        print("🛑 Exiting...")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
