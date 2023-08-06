function alertLayers(document: Document): void {

    var layers = document.layers;
    var alertString = "このドキュメントには" + String(layers.length) + "個のレイヤーがあります\n";

    var i: number;
    for (i = 0; i < layers.length; i++) {
        var layer: Layer = layers[i];
        alertString += "- " + layer.name + "\n";
    }

    alert(alertString);
}

export default alertLayers;