#!/usr/bin/env python3
"""
Script to remove emojis from all files in the project.
"""
import os
import re
import sys


def remove_emojis(text):
    """Remove emojis from text using regex pattern for Unicode emoji ranges.

    Returns:
        tuple: (cleaned_text, count_of_emojis_removed)
    """
    # Comprehensive emoji pattern covering various Unicode blocks (without + quantifier)
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # emoticons
        "\U0001f300-\U0001f5ff"  # misc symbols & pictographs
        "\U0001f680-\U0001f6ff"  # transport & map symbols
        "\U0001f1e0-\U0001f1ff"  # flags (iOS)
        "\U00002700-\U000027bf"  # dingbats
        "\U0001f926-\U0001f937"  # gestures
        "\U00010000-\U0010ffff"  # other Unicode planes
        "\U00002702-\U000027b0"  # more dingbats
        "\U000024c2-\U0001f251"  # enclosed alphanumerics
        "\u200d"  # zero width joiner
        "\u23cf"  # eject symbol
        "\u23e9"  # fast forward
        "\u231a"  # watch
        "\u231b"  # hourglass
        "\u2328"  # keyboard
        "\u23f0"  # alarm clock
        "\u23f3"  # hourglass flowing sand
        "\u25aa"  # black small square
        "\u25ab"  # white small square
        "\u25b6"  # play button
        "\u25c0"  # reverse button
        "\u25fb"  # white medium square
        "\u25fc"  # black medium square
        "\u25fd"  # white medium small square
        "\u25fe"  # black medium small square
        "\u2600"  # sun
        "\u2601"  # cloud
        "\u2602"  # umbrella
        "\u2603"  # snowman
        "\u2604"  # comet
        "\u2605"  # star
        "\u2606"  # white star
        "\u2607"  # lightning
        "\u2608"  # thunderstorm
        "\u2609"  # sun behind cloud
        "\u260a"  # crescent moon
        "\u260b"  # shooting star
        "\u260c"  # waxing crescent moon
        "\u260d"  # waning crescent moon
        "\u260e"  # telephone
        "\u260f"  # white telephone
        "\u2610"  # ballot box
        "\u2611"  # ballot box with check
        "\u2612"  # ballot box with x
        "\u2613"  # saltire
        "\u2614"  # umbrella with rain drops
        "\u2615"  # hot beverage
        "\u2616"  # white shogi piece
        "\u2617"  # black shogi piece
        "\u2618"  # shamrock
        "\u2619"  # reversed rotated floral heart bullet
        "\u2620"  # skull and crossbones
        "\u2621"  # caution sign
        "\u2622"  # radioactive sign
        "\u2623"  # biohazard sign
        "\u2624"  # caduceus
        "\u2625"  # ankh
        "\u2626"  # orthodox cross
        "\u2627"  # chi rho
        "\u2628"  # cross of loraine
        "\u2629"  # cross of jerusalem
        "\u2630"  # trigrams
        "\u2631"  # trigrams
        "\u2632"  # trigrams
        "\u2633"  # trigrams
        "\u2634"  # trigrams
        "\u2635"  # trigrams
        "\u2636"  # trigrams
        "\u2637"  # trigrams
        "\u2638"  # wheel of dharma
        "\u2639"  # white frowning face
        "\u263a"  # white smiling face
        "\u2640"  # female sign
        "\u2641"  # earth
        "\u2642"  # male sign
        "\u2643"  # jupiter
        "\u2644"  # saturn
        "\u2645"  # uranus
        "\u2646"  # neptune
        "\u2647"  # pluto
        "\u2648"  # aries
        "\u2649"  # taurus
        "\u2650"  # gemini
        "\u2651"  # cancer
        "\u2652"  # leo
        "\u2653"  # virgo
        "\u2654"  # libra
        "\u2655"  # scorpius
        "\u2656"  # ophiuchus
        "\u2657"  # sagittarius
        "\u2658"  # capricorn
        "\u2659"  # aquarius
        "\u265a"  # pisces
        "\u265b"  # earth
        "\u265c"  # sextile
        "\u265d"  # opposition
        "\u265e"  # conjunction
        "\u265f"  # alchemical symbol for iron ore
        "\u2660"  # spade suit
        "\u2661"  # heart suit
        "\u2662"  # diamond suit
        "\u2663"  # club suit
        "\u2664"  # white spade suit
        "\u2665"  # white heart suit
        "\u2666"  # white diamond suit
        "\u2667"  # white club suit
        "\u2668"  # hot springs
        "\u2669"  # quarter note
        "\u266a"  # eighth note
        "\u266b"  # beamed eighth notes
        "\u266c"  # beamed sixteenth notes
        "\u266d"  # music flat sign
        "\u266e"  # music natural sign
        "\u266f"  # music sharp sign
        "\u2670"  # west syriac cross
        "\u2671"  # east syriac cross
        "\u2672"  # universal recycling symbol
        "\u2673"  # recycling symbol for type-1 plastics
        "\u2674"  # recycling symbol for type-2 plastics
        "\u2675"  # recycling symbol for type-3 plastics
        "\u2676"  # recycling symbol for type-4 plastics
        "\u2677"  # recycling symbol for type-5 plastics
        "\u2678"  # recycling symbol for type-6 plastics
        "\u2679"  # recycling symbol for type-7 plastics
        "\u267a"  # recycling symbol for type-1 plastics
        "\u267b"  # recycling symbol for type-2 plastics
        "\u267c"  # recycling symbol for type-3 plastics
        "\u267d"  # recycling symbol for type-4 plastics
        "\u267e"  # recycling symbol for type-5 plastics
        "\u267f"  # recycling symbol for type-6 plastics
        "\u2680"  # die face-1
        "\u2681"  # die face-2
        "\u2682"  # die face-3
        "\u2683"  # die face-4
        "\u2684"  # die face-5
        "\u2685"  # die face-6
        "\u2686"  # white circle with dot right
        "\u2687"  # white circle with two dots
        "\u2688"  # black circle with white dot right
        "\u2689"  # black circle with two white dots
        "\u268a"  # monochrome picture
        "\u268b"  # black square button
        "\u268c"  # white square button
        "\u268d"  # black square button
        "\u268e"  # white square button
        "\u268f"  # black square button
        "\u2690"  # white square button
        "\u2691"  # black flag
        "\u2692"  # hammer and pick
        "\u2693"  # anchor
        "\u2694"  # crossed swords
        "\u2695"  # staff of aesculapius
        "\u2696"  # scales of justice
        "\u2697"  # alembic
        "\u2698"  # flower
        "\u2699"  # gear
        "\u269a"  # staff of hermes
        "\u269b"  # atom symbol
        "\u269c"  # fleur-de-lis
        "\u269d"  # outlined white star
        "\ufe0f"  # variation selector-16
        "]+",
        flags=re.UNICODE,
    )

    # Create a pattern that matches individual emoji characters (without + quantifier)
    individual_emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # emoticons
        "\U0001f300-\U0001f5ff"  # misc symbols & pictographs
        "\U0001f680-\U0001f6ff"  # transport & map symbols
        "\U0001f1e0-\U0001f1ff"  # flags (iOS)
        "\U00002700-\U000027bf"  # dingbats
        "\U0001f926-\U0001f937"  # gestures
        "\U00010000-\U0010ffff"  # other Unicode planes
        "\U00002702-\U000027b0"  # more dingbats
        "\U000024c2-\U0001f251"  # enclosed alphanumerics
        "\u200d"  # zero width joiner
        "\u23cf"  # eject symbol
        "\u23e9"  # fast forward
        "\u231a"  # watch
        "\u231b"  # hourglass
        "\u2328"  # keyboard
        "\u23f0"  # alarm clock
        "\u23f3"  # hourglass flowing sand
        "\u25aa"  # black small square
        "\u25ab"  # white small square
        "\u25b6"  # play button
        "\u25c0"  # reverse button
        "\u25fb"  # white medium square
        "\u25fc"  # black medium square
        "\u25fd"  # white medium small square
        "\u25fe"  # black medium small square
        "\u2600"  # sun
        "\u2601"  # cloud
        "\u2602"  # umbrella
        "\u2603"  # snowman
        "\u2604"  # comet
        "\u2605"  # star
        "\u2606"  # white star
        "\u2607"  # lightning
        "\u2608"  # thunderstorm
        "\u2609"  # sun behind cloud
        "\u260a"  # crescent moon
        "\u260b"  # shooting star
        "\u260c"  # waxing crescent moon
        "\u260d"  # waning crescent moon
        "\u260e"  # telephone
        "\u260f"  # white telephone
        "\u2610"  # ballot box
        "\u2611"  # ballot box with check
        "\u2612"  # ballot box with x
        "\u2613"  # saltire
        "\u2614"  # umbrella with rain drops
        "\u2615"  # hot beverage
        "\u2616"  # white shogi piece
        "\u2617"  # black shogi piece
        "\u2618"  # shamrock
        "\u2619"  # reversed rotated floral heart bullet
        "\u2620"  # skull and crossbones
        "\u2621"  # caution sign
        "\u2622"  # radioactive sign
        "\u2623"  # biohazard sign
        "\u2624"  # caduceus
        "\u2625"  # ankh
        "\u2626"  # orthodox cross
        "\u2627"  # chi rho
        "\u2628"  # cross of loraine
        "\u2629"  # cross of jerusalem
        "\u2630"  # trigrams
        "\u2631"  # trigrams
        "\u2632"  # trigrams
        "\u2633"  # trigrams
        "\u2634"  # trigrams
        "\u2635"  # trigrams
        "\u2636"  # trigrams
        "\u2637"  # trigrams
        "\u2638"  # wheel of dharma
        "\u2639"  # white frowning face
        "\u263a"  # white smiling face
        "\u2640"  # female sign
        "\u2641"  # earth
        "\u2642"  # male sign
        "\u2643"  # jupiter
        "\u2644"  # saturn
        "\u2645"  # uranus
        "\u2646"  # neptune
        "\u2647"  # pluto
        "\u2648"  # aries
        "\u2649"  # taurus
        "\u2650"  # gemini
        "\u2651"  # cancer
        "\u2652"  # leo
        "\u2653"  # virgo
        "\u2654"  # libra
        "\u2655"  # scorpius
        "\u2656"  # ophiuchus
        "\u2657"  # sagittarius
        "\u2658"  # capricorn
        "\u2659"  # aquarius
        "\u265a"  # pisces
        "\u265b"  # earth
        "\u265c"  # sextile
        "\u265d"  # opposition
        "\u265e"  # conjunction
        "\u265f"  # alchemical symbol for iron ore
        "\u2660"  # spade suit
        "\u2661"  # heart suit
        "\u2662"  # diamond suit
        "\u2663"  # club suit
        "\u2664"  # white spade suit
        "\u2665"  # white heart suit
        "\u2666"  # white diamond suit
        "\u2667"  # white club suit
        "\u2668"  # hot springs
        "\u2669"  # quarter note
        "\u266a"  # eighth note
        "\u266b"  # beamed eighth notes
        "\u266c"  # beamed sixteenth notes
        "\u266d"  # music flat sign
        "\u266e"  # music natural sign
        "\u266f"  # music sharp sign
        "\u2670"  # west syriac cross
        "\u2671"  # east syriac cross
        "\u2672"  # universal recycling symbol
        "\u2673"  # recycling symbol for type-1 plastics
        "\u2674"  # recycling symbol for type-2 plastics
        "\u2675"  # recycling symbol for type-3 plastics
        "\u2676"  # recycling symbol for type-4 plastics
        "\u2677"  # recycling symbol for type-5 plastics
        "\u2678"  # recycling symbol for type-6 plastics
        "\u2679"  # recycling symbol for type-7 plastics
        "\u267a"  # recycling symbol for type-1 plastics
        "\u267b"  # recycling symbol for type-2 plastics
        "\u267c"  # recycling symbol for type-3 plastics
        "\u267d"  # recycling symbol for type-4 plastics
        "\u267e"  # recycling symbol for type-5 plastics
        "\u267f"  # recycling symbol for type-6 plastics
        "\u2680"  # die face-1
        "\u2681"  # die face-2
        "\u2682"  # die face-3
        "\u2683"  # die face-4
        "\u2684"  # die face-5
        "\u2685"  # die face-6
        "\u2686"  # white circle with dot right
        "\u2687"  # white circle with two dots
        "\u2688"  # black circle with white dot right
        "\u2689"  # black circle with two white dots
        "\u268a"  # monochrome picture
        "\u268b"  # black square button
        "\u268c"  # white square button
        "\u268d"  # black square button
        "\u268e"  # white square button
        "\u268f"  # black square button
        "\u2690"  # white square button
        "\u2691"  # black flag
        "\u2692"  # hammer and pick
        "\u2693"  # anchor
        "\u2694"  # crossed swords
        "\u2695"  # staff of aesculapius
        "\u2696"  # scales of justice
        "\u2697"  # alembic
        "\u2698"  # flower
        "\u2699"  # gear
        "\u269a"  # staff of hermes
        "\u269b"  # atom symbol
        "\u269c"  # fleur-de-lis
        "\u269d"  # outlined white star
        "\ufe0f"  # variation selector-16
        "]",
        flags=re.UNICODE,
    )

    # Count individual emoji characters using findall with the pattern without + quantifier
    emoji_matches = individual_emoji_pattern.findall(text)
    count = len(emoji_matches)

    # Remove emojis from text using the original pattern with + quantifier for proper cleanup
    cleaned_text = emoji_pattern.sub("", text)

    return cleaned_text, count


def should_process_file(file_path):
    """Check if file should be processed (text files only, skip binary and venv)."""
    # Skip files in virtual environment
    if ".venv" in file_path or "__pycache__" in file_path:
        return False
    # Skip binary files and certain extensions
    binary_extensions = {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".ico",
        ".zip",
        ".tar",
        ".gz",
        ".exe",
        ".dll",
        ".so",
        ".dylib",
    }
    if any(file_path.lower().endswith(ext) for ext in binary_extensions):
        return False
    # Only process text files
    text_extensions = {
        ".py",
        ".md",
        ".txt",
        ".sh",
        ".bat",
        ".ini",
        ".json",
        ".yaml",
        ".yml",
        ".xml",
        ".html",
        ".css",
        ".js",
        ".ts",
    }
    return any(file_path.lower().endswith(ext) for ext in text_extensions)


def process_files(root_dir):
    """Process all files in the directory tree and remove emojis.

    Returns:
        tuple: (files_processed, files_modified, modified_files_info)
        where modified_files_info is a dict mapping file paths to emoji counts
    """
    files_processed = 0
    files_modified = 0
    modified_files_info = {}  # Track file paths and their emoji counts

    for root, dirs, files in os.walk(root_dir):
        # Skip virtual environment and cache directories
        dirs[:] = [d for d in dirs if d not in {".venv", "__pycache__", ".git"}]
        for file in files:
            file_path = os.path.join(root, file)
            if not should_process_file(file_path):
                continue
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    original_content = f.read()
                # Remove emojis and get count
                cleaned_content, emoji_count = remove_emojis(original_content)
                # Check if content changed
                if cleaned_content != original_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(cleaned_content)
                    files_modified += 1
                    modified_files_info[file_path] = emoji_count
                    print(f"Modified: {file_path} (removed {emoji_count} emojis)")
                files_processed += 1
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    return files_processed, files_modified, modified_files_info


def main():
    """Main function."""
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = "."
    print(f"Removing emojis from files in {root_dir}...")
    files_processed, files_modified, modified_files_info = process_files(root_dir)

    # Calculate total emojis removed
    total_emojis_removed = sum(modified_files_info.values())

    # Display summary
    print(f"\n=== EMOJI REMOVAL SUMMARY ===")
    print(f"Files processed: {files_processed}")
    print(f"Files modified: {files_modified}")
    print(f"Total emojis removed: {total_emojis_removed}")

    # Display detailed file information if any files were modified
    if modified_files_info:
        print(f"\n=== FILES MODIFIED ===")
        for file_path, emoji_count in sorted(modified_files_info.items()):
            print(f"{file_path}: {emoji_count} emojis removed")
    else:
        print(f"\nNo emoji-containing files were found.")


if __name__ == "__main__":
    main()
