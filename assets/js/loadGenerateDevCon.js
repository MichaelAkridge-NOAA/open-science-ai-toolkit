function generateDevContainerJSON() {
    const name = document.getElementById('nameField').value;
    const workspaceFolder = document.getElementById('workspaceField').value;
    const cpus = document.getElementById('cpuSelector').value;
    const extensions = Array.from(document.getElementById('extensionSelector').selectedOptions).map(opt => opt.value);
    const rawPorts = document.getElementById('ports').value;
    const ports = rawPorts.split(',').map(port => port.trim()).filter(port => port !== ''); // Filters out empty entries
    const baseImageURL = "ghcr.io/nmfs-opensci/";
    const selectedImage = document.getElementById('packageSelector').value;
    const image = baseImageURL + selectedImage;

    let devContainerConfig = {
        "name": name,
        "workspaceFolder": workspaceFolder,
        "image": image,
        "hostRequirements": {
            "cpus": cpus
        },
        "customizations": {
            "vscode": {
                "extensions": extensions
            }
        }
    };

    // Optional commands
    ["updateContentCommand", "postCreateCommand", "postStartCommand"].forEach(cmd => {
        const commandValue = document.getElementById(cmd).value.trim();
        if (commandValue) {
            devContainerConfig[cmd] = commandValue;
        }
    });

    if (ports.length > 0) {
        devContainerConfig.forwardPorts = ports.map(Number);
        devContainerConfig.portsAttributes = {};
        ports.forEach(port => {
            devContainerConfig.portsAttributes[port] = {
                "label": selectedImage,
                "onAutoForward": "openPreview"
            };
        });
    }

    globalJSON = JSON.stringify(devContainerConfig, null, 2);
    document.getElementById('output').textContent = globalJSON;
    document.getElementById('downloadBtn').style.display = 'inline-block';
}

