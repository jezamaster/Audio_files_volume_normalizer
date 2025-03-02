import os
from pydub import AudioSegment

def get_audio_volume(input_file):
    # Load the audio file
    audio = AudioSegment.from_wav(input_file)

    # Get the average dBFS of the audio
    return audio.dBFS

def display_volumes_in_directory(input_directory):
    # Iterate over all files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".wav"):
            input_file = os.path.join(input_directory, filename)
            
            # Get the volume level in dBFS
            volume = get_audio_volume(input_file)
            
            # Display the filename and volume level
            print(f"Song: {filename} | Volume: {volume:.2f} dBFS")
    
    # If request to normalize, enter the required negative value of decibels
    try:
        target_dBFS = float(input("\n\nEnter the target dBFS to normalize to (MUST BE NEGATIVE, e.g. -10), the closer to zero, the louder: "))
    except ValueError:
        # Exit the program if the input is not a valid number
        exit()
    else:
        normalize_to_target_dBFS(input_directory, target_dBFS)
        
def normalize_to_target_dBFS(input_directory, target_dBFS):
    # Create a subdirectory called 'normalized' within the input directory
    output_directory = os.path.join(input_directory, "normalized")
    
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    else:
        print(f"Directory 'normalized' already exists.")

    # Iterate over all files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".wav"):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, filename)
            
            # Load the audio file
            audio = AudioSegment.from_wav(input_file)
            
            # Calculate the gain to apply to normalize to the target dBFS
            change_in_dBFS = target_dBFS - audio.dBFS
            
            # Apply the gain
            normalized_audio = audio.apply_gain(change_in_dBFS)
            
            # Export the normalized audio
            normalized_audio.export(output_file, format="wav")
            print(f"Normalized {filename} to {target_dBFS} dBFS and saved to {output_file}")

# Example usage
try:
    input_directory = input("path_to_your_input_wav_files: ")
except Exception as e:
    print("Error: ", e)
else:
    display_volumes_in_directory(input_directory)
