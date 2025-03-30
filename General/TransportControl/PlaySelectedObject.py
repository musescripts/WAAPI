from waapi import WaapiClient

# Initialize global variables
lastSelectedID = None
lastTransportID = None

def controlSelectedTransport():
    global lastSelectedID, lastTransportID
    try:
        # Connect to WAAPI
        with WaapiClient() as client:
            # Get the selected object
            getSelection = {"options": {"return": ["id", "name", "type"]}}
            selection = client.call("ak.wwise.ui.getSelectedObjects", getSelection)

            # Check if a valid object is selected
            if selection and selection["objects"]:
                firstSelected = selection["objects"][0]
                currentSelectedID = firstSelected['id']

                if currentSelectedID == lastSelectedID and lastTransportID is not None:
                    transportID = lastTransportID
                else:
                    # Get a list of transport objects
                    getTransportList = client.call("ak.wwise.core.transport.getList").get("list", [])
                    currentTransport = next((t for t in getTransportList if t.get("object") == currentSelectedID), None)

                    if currentTransport:
                        transportID = currentTransport["transport"]
                    else:
                        # Create transport object for the selected item
                        createTransport = {"object": firstSelected["id"]}
                        transportResponse = client.call("ak.wwise.core.transport.create", createTransport)
                        transportID = transportResponse["transport"]

                    lastSelectedID = currentSelectedID
                    lastTransportID = transportID

                # Execute play action on the transport
                playAction = {"transport": transportID, "action": "play"}
                client.call("ak.wwise.core.transport.executeAction", playAction)

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    controlSelectedTransport()
