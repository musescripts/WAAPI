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

                # Create transport object for the selected item
                createTransport = {"object": firstSelected["id"]}
                transport = client.call("ak.wwise.core.transport.create", createTransport)

                # Execute play action on the transport
                playAction = {"transport": transport["transport"], "action": "play"}
                client.call("ak.wwise.core.transport.executeAction", playAction)

    except Exception as e:
        pass


if __name__ == "__main__":
    controlSelectedTransport()
