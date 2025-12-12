# Contributing to Pylontech Serial Integration

Thank you for your interest in contributing! This guide primarily focuses on adding support for new USB-to-Serial adapters for auto-discovery.

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

### 3. Submit a Pull Request

Create a Pull Request with your changes. Please include the output of `lsusb` or the device model name in your PR description so we can verify it.
