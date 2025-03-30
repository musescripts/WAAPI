from waapi import WaapiClient


def controlSelectedTransport():
    try:
        # Connect to WAAPI
        with WaapiClient() as client:
            # Get the selected object
            getSelection = {"options": {"return": ["id", "name", "type"]}}
            selection = client.call("ak.wwise.ui.getSelectedObjects", getSelection)

            # Check if a valid object is selected
            if selection and selection["objects"]:
                firstSelected = selection["objects"][0]
                firstSelectedID = firstSelected['id']

                # Get the transport list
                getTransportList = client.call("ak.wwise.core.transport.getList").get("list", [])

                #Find the transport associated with the selected object
                currentTransport = next((t for t in getTransportList if t.get("object") == firstSelectedID), None)

                # Destroy the transport
                if currentTransport:
                    transportID = currentTransport["transport"]
                    client.call("ak.wwise.core.transport.destroy", {"transport" :transportID})

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    controlSelectedTransport()