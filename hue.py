from bluepy import btle

MAC = "DA:3C:2F:A3:65:B7"

p = btle.Peripheral(MAC, btle.ADDR_TYPE_RANDOM)

skip = [
    btle.UUID("932c32bd-0002-47a2-835a-a8d455b859dd"),
    btle.UUID("b8843add-0001-4aa1-8794-c3f462030bda"),
    btle.UUID("b8843add-0004-4aa1-8794-c3f462030bda")
]

SERVICE_UUID = "932c32bd-0000-47a2-835a-a8d455b859dd"
CHAR_UUID = "932c32bd-0002-47a2-835a-a8d455b859dd"

p.setSecurityLevel("medium")

try:
    service = p.getServiceByUUID(SERVICE_UUID)
    print(f"Got service with UUID {service.uuid}")

    chars = service.getCharacteristics(CHAR_UUID)
    if len(chars) == 0:
        print("Failed to get the on/off characteristic :(")
    else:
        onoff = chars[0]
        print(f"Got the on/off characteristic with UUID {onoff.uuid} and handle 0x{onoff.handle:02X}")

        if onoff.supportsRead():
            print("Reading its value")
            value = onoff.read()

            hx = ":".join(f"{x:02X}" for x in value)

            print(f"data = {hx}")

            on = len(value) > 0 and value[0] == 1
            print(f"is on? {on}")

            print("Toggle!")
            if on:
                onoff.write(b"\x00", withResponse=True)
            else:
                onoff.write(b"\x01", withResponse=True)



except Exception as e:
    print("ERROR")
    print(e)
finally:
    print("Disconnecting")
    p.disconnect()
