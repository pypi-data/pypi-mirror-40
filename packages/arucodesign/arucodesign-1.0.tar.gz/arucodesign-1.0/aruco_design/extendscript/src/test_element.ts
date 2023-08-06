function alertElements(document: Document): void {

    var layers = document.layers;
    var alertString = "Item Structure of " + String(document) + ": \n";

    for (var i: number = 0; i < layers.length; i++) {
        var layer: Layer = layers[i];
        var items = layer.pageItems;

        alertString += layer.name + '\n';
        for (var j: number = 0; j < items.length; j++) {
            var item: PageItem = items[j];
            var itemDescription = String(item.name) + ': ' + String(item.typename) + ', ' + String(item.position);
            alertString += '\t- ' + itemDescription + '\n';
        }
    }

    alert(alertString);
}

export default alertElements;