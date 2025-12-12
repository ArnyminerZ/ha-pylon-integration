# Contributing to Pylontech Serial Integration

Thank you for your interest in contributing! This guide covers adding support for new USB devices and translating the integration into other languages.

## Adding Support for New USB Devices

Currently, the integration is configured to automatically discover specific USB adapters (like the Prolific PL2303). If your adapter is not detected automatically, you can help us support it!

### 1. Identify your Device's VID and PID

You need to find the **Vendor ID (VID)** and **Product ID (PID)** of your USB adapter.

**On Linux (including Home Assistant OS via SSH):**
1. Plug in your USB adapter.
2. Run the `lsusb` command.
3. Look for a line that corresponds to your serial adapter. It will look something like this:
   ```
   Bus 001 Device 004: ID 067b:2303 Prolific Technology, Inc. PL2303 Serial Port
   ```
   In this example:
   - **VID** is `067B`
   - **PID** is `2303`

### 2. Update `manifest.json`

1. Open `custom_components/pylontech_serial/manifest.json`.
2. Locate the `"usb"` section.
3. Add a new entry with your VID and PID. Note that the keys are case-sensitive and should usually be uppercase.

```json
  "usb": [
    {
      "vid": "067B",
      "pid": "2303"
    },
    {
      "vid": "YOUR_NEW_VID",
      "pid": "YOUR_NEW_PID"
    }
  ],
```

## Adding Translations

We welcome translations to make this integration accessible to everyone!

1. **Locate the Translations**: Go to `custom_components/pylontech_serial/translations/`.
2. **Create your Language File**:
    - Find the English file: `en.json`.
    - Copy it and name the new file with your language's ISO 639-1 code (e.g., `es.json` for Spanish, `fr.json` for French, `de.json` for German).
3. **Translate**:
    - Open your new file (e.g., `es.json`).
    - Translate the values on the right side of the colon. **Do not change the keys** (the text on the left).

   **Example (`es.json`):**
   ```json
   {
     "config": {
       "step": {
         "user": {
           "data": {
             "serial_port": "Puerto Serie"
           }
         }
       }
     }
   }
   ```

## Submitting a Pull Request

1. Create a Pull Request with your changes.
2. If adding a device, include the `lsusb` output.
3. If adding a translation, mention the language you are adding.
