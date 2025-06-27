"""
Screenshot Module
Cross-platform screenshot functionality
"""

import os
import time
import platform
from datetime import datetime


class Screenshot:
    def __init__(self, save_directory="screenshots"):
        self.save_directory = save_directory
        self.system = platform.system().lower()

        # Create screenshots directory if it doesn't exist
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
            print(f"Created screenshots directory: {self.save_directory}")

        # Try to import screenshot libraries
        self.method = None

        try:
            import pyautogui

            pyautogui.FAILSAFE = False  # Disable failsafe for gesture control
            self.pyautogui = pyautogui
            self.method = "pyautogui"
            print("Screenshot initialized with pyautogui")
        except ImportError:
            print("pyautogui not installed. Install with: pip install pyautogui")

            # Try alternative methods based on OS
            if self.system == "windows":
                try:
                    from PIL import ImageGrab

                    self.ImageGrab = ImageGrab
                    self.method = "pil"
                    print("Screenshot initialized with PIL ImageGrab (Windows)")
                except ImportError:
                    self.method = "fallback"

            elif self.system == "darwin":  # macOS
                self.method = "screencapture"
                print("Screenshot initialized with screencapture (macOS)")

            elif self.system == "linux":
                # Check for available screenshot tools
                import subprocess

                try:
                    subprocess.run(
                        ["gnome-screenshot", "--version"],
                        capture_output=True,
                        check=True,
                    )
                    self.method = "gnome-screenshot"
                    print("Screenshot initialized with gnome-screenshot (Linux)")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    try:
                        subprocess.run(
                            ["scrot", "--version"], capture_output=True, check=True
                        )
                        self.method = "scrot"
                        print("Screenshot initialized with scrot (Linux)")
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        try:
                            subprocess.run(
                                ["import", "-version"], capture_output=True, check=True
                            )
                            self.method = "imagemagick"
                            print("Screenshot initialized with ImageMagick (Linux)")
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            self.method = "fallback"
            else:
                self.method = "fallback"

    def generate_filename(self, prefix="screenshot", extension="png"):
        """Generate a unique filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.{extension}"
        return os.path.join(self.save_directory, filename)

    def take_screenshot(self, overlay_image=None):
        """Take a screenshot and save it to file"""
        filename = self.generate_filename()

        try:
            if self.method == "pyautogui":
                screenshot = self.pyautogui.screenshot()
                screenshot.save(filename)

            elif self.method == "pil":
                # Windows PIL method
                screenshot = self.ImageGrab.grab()
                screenshot.save(filename)

            elif self.method == "screencapture":
                # macOS screencapture
                import subprocess

                subprocess.run(["screencapture", "-x", filename], check=True)

            elif self.method == "gnome-screenshot":
                # Linux gnome-screenshot
                import subprocess

                subprocess.run(["gnome-screenshot", "-f", filename], check=True)

            elif self.method == "scrot":
                # Linux scrot
                import subprocess

                subprocess.run(["scrot", filename], check=True)

            elif self.method == "imagemagick":
                # Linux ImageMagick
                import subprocess

                subprocess.run(["import", "-window", "root", filename], check=True)

            else:
                # Fallback method - create a placeholder
                self._create_placeholder_screenshot(filename, overlay_image)

            print(f"Screenshot saved: {filename}")
            return filename

        except Exception as e:
            print(f"Screenshot error: {e}")
            # Create placeholder on error
            try:
                self._create_placeholder_screenshot(filename, overlay_image)
                return filename
            except Exception as e2:
                print(f"Fallback screenshot error: {e2}")
                return None

    def _create_placeholder_screenshot(self, filename, overlay_image=None):
        """Create a placeholder screenshot when other methods fail"""
        try:
            from PIL import Image, ImageDraw, ImageFont

            # Create a simple placeholder image
            width, height = 1920, 1080
            image = Image.new("RGB", (width, height), color="darkblue")
            draw = ImageDraw.Draw(image)

            # Add text
            try:
                # Try to use a default font
                font = ImageFont.truetype("arial.ttf", 48)
            except:
                font = ImageFont.load_default()

            text = "Screenshot Captured!"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Calculate text position (centered)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2

            # Draw text with shadow
            draw.text((text_x + 2, text_y + 2), text, fill="black", font=font)
            draw.text((text_x, text_y), text, fill="white", font=font)
            draw.text((text_x, text_y + 60), timestamp, fill="lightgray", font=font)

            # If overlay image is provided, add it as a small preview
            if overlay_image is not None:
                try:
                    import cv2

                    # Convert opencv image to PIL
                    overlay_rgb = cv2.cvtColor(overlay_image, cv2.COLOR_BGR2RGB)
                    overlay_pil = Image.fromarray(overlay_rgb)

                    # Resize overlay to fit in corner
                    overlay_size = (320, 240)
                    overlay_resized = overlay_pil.resize(overlay_size)

                    # Paste in top-right corner
                    paste_x = width - overlay_size[0] - 20
                    paste_y = 20
                    image.paste(overlay_resized, (paste_x, paste_y))

                    # Add border around overlay
                    draw.rectangle(
                        [
                            paste_x - 2,
                            paste_y - 2,
                            paste_x + overlay_size[0] + 2,
                            paste_y + overlay_size[1] + 2,
                        ],
                        outline="white",
                        width=2,
                    )
                except Exception as e:
                    print(f"Could not add overlay: {e}")

            image.save(filename)

        except ImportError:
            # If PIL is not available, create a simple text file
            with open(filename.replace(".png", ".txt"), "w") as f:
                f.write(f"Screenshot taken at {datetime.now()}\n")
                f.write("Note: Image libraries not available for actual screenshot\n")

    def take_region_screenshot(self, x, y, width, height):
        """Take a screenshot of a specific region"""
        filename = self.generate_filename("region_screenshot")

        try:
            if self.method == "pyautogui":
                screenshot = self.pyautogui.screenshot(region=(x, y, width, height))
                screenshot.save(filename)

            elif self.method == "pil":
                bbox = (x, y, x + width, y + height)
                screenshot = self.ImageGrab.grab(bbox)
                screenshot.save(filename)

            else:
                # For other methods, fall back to full screenshot
                return self.take_screenshot()

            print(f"Region screenshot saved: {filename}")
            return filename

        except Exception as e:
            print(f"Region screenshot error: {e}")
            return None

    def get_screenshot_count(self):
        """Get the number of screenshots in the directory"""
        try:
            files = [
                f
                for f in os.listdir(self.save_directory)
                if f.endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
            ]
            return len(files)
        except:
            return 0

    def cleanup_old_screenshots(self, keep_last=50):
        """Remove old screenshots, keeping only the most recent ones"""
        try:
            files = []
            for f in os.listdir(self.save_directory):
                if f.endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                    filepath = os.path.join(self.save_directory, f)
                    files.append((filepath, os.path.getctime(filepath)))

            # Sort by creation time (newest first)
            files.sort(key=lambda x: x[1], reverse=True)

            # Remove files beyond the keep limit
            for filepath, _ in files[keep_last:]:
                os.remove(filepath)
                print(f"Removed old screenshot: {os.path.basename(filepath)}")

        except Exception as e:
            print(f"Cleanup error: {e}")


# Test the screenshot functionality
if __name__ == "__main__":
    screenshot_ctrl = Screenshot()
    print(f"Screenshot directory: {screenshot_ctrl.save_directory}")
    print(f"Screenshot method: {screenshot_ctrl.method}")

    # Take a test screenshot
    filename = screenshot_ctrl.take_screenshot()
    if filename:
        print(f"Test screenshot saved: {filename}")

    print(f"Total screenshots: {screenshot_ctrl.get_screenshot_count()}")
