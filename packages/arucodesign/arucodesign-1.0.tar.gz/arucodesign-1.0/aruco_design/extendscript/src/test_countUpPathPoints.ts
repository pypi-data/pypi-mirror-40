import 'extendscript-es5-shim-ts';


function main(document: Document): void {
    const layers = document.layers;
    let alertString: string = "Result:\n";

    for (var i: number = 0; i < layers.length; i++) {
        var layer: Layer = layers[i];
        var pathItems = layer.pathItems;
        for (var j: number = 0; j < pathItems.length; j++) {
            var pathItem: PathItem = pathItems[j];
            alertString += 'On pathItem' + String(pathItem.position) + ':\n';
            var pathPoints = pathItem.pathPoints;
            for (var k: number = 0; k < pathPoints.length; k++) {
                var pathPoint: PathPoint = pathPoints[k];
                alertString += String(pathPoint.anchor) + ',' + pathPoint.typename + '\n';
                alertString += String(pathPoint.pointType) + '\n';
            }
        }
    }

    alert(alertString);
}

main(app.activeDocument);