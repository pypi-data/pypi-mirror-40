import 'extendscript-es5-shim-ts';
import * as aruco from './lib/aruco';

function main(document: Document): void {
    const layers = document.layers;
    const arucoMarkerPath: string = '~/Downloads/aruco6x6_250/';
    const placedItems: PlacedItems = document.placedItems;

    let markerNum = 0;

    // for (var i: number = 0; i < layers.length; i++) {
    for (var i: number = 0; i < 1; i++) {
        var layer: Layer = layers[i + 1];
        var pathItems = layer.pathItems;
        for (var j: number = 0; j < pathItems.length; j++) {
            var pathItem: PathItem = pathItems[j];
            var pathPoints = pathItem.pathPoints;
            for (var k: number = 0; k < pathPoints.length; k++) {
                var pathPoint: PathPoint = pathPoints[k];
                var newMarker: PlacedItem = placedItems.add();
                newMarker.file = new File(arucoMarkerPath + aruco.arucoFileName(markerNum + 4));
                let newPosition = pathPoint.anchor;
                newPosition[0] -= newMarker.width / 2;
                newPosition[1] += newMarker.height / 2;
                newMarker.position = newPosition;
                newMarker.resize(1000 / newMarker.width, 1000 / newMarker.height);
                // newMarker.embed();
                markerNum++;
            }
        }
    }
}

main(app.activeDocument);