import 'extendscript-es5-shim-ts';
import * as aruco from './lib/aruco';
import * as P from './lib/position';
import * as IO from './lib/io';
import alertLayers from './test_layer';


function main(document: Document): void {
    const layers = document.layers;

    const layerForObjects: Layer = layers[0];
    const layerForMarker: Layer = aruco.addLayerForArucoMarker(document);
    const container = P.IllustratorObjectContainer.getInstance();

    let markerNum = 0;
    let linkArray = new Array<P.Link>();

    // sweep pathItems
    for (var i: number = 0; i < layerForObjects.pathItems.length; i++) {
        var pathItem: PathItem = layerForObjects.pathItems[i];
        var itemInfo: P.IllustratorObject = new P.IllustratorObject(pathItem, 'object');
        var pathPoints: PathPoints = pathItem.pathPoints;

        for (var j: number = 0; j < pathPoints.length; j++) {
            var pathPoint = pathPoints[j];
            var pointInfo = new P.IllustratorObject(pathPoint, 'marker');
            pointInfo.belongsTo = itemInfo;
            if (j > 0 && j < pathPoints.length) linkArray.push(new P.Link(pointInfo, container.getItem('marker', markerNum)));
            if (j === (pathPoints.length - 1) && pathItem.closed) linkArray.push(new P.Link(pointInfo, container.getItem('marker', markerNum - j + 1)));

            aruco.embedMarker(pointInfo.id, layerForMarker, pathPoint, 1000);
            markerNum++;
        }
    }

    // sweep groupItems as one pathItem
    for (var i: number = 0; i < layerForObjects.groupItems.length; i++) {
        var groupItem = layerForObjects.groupItems[i];
        var itemInfo = new P.IllustratorObject(groupItem, 'object');
        var pathItems = groupItem.pathItems;
        var allPathPoints = new Array<P.IllustratorObject>();
        for (var j: number = 0; j < pathItems.length; j++) {
            var pathItem: PathItem = pathItems[j];
            var pathPoints: PathPoints = pathItem.pathPoints;
            var previousPointInfo: P.IllustratorObject = null;
            var firstPointInfo: P.IllustratorObject = null;

            for (var k: number = 0; k < pathPoints.length; k++) {
                var pathPoint = pathPoints[k];
                var pointAlreadyDeclared: number = -1;
                // check if same point already exists
                for (var l: number = 0; l < allPathPoints.length; l++) {
                    var oldPointInfo = allPathPoints[l];
                    if (Math.abs(oldPointInfo.position.anchor.x - pathPoint.anchor[0]) < 1
                        && Math.abs(oldPointInfo.position.anchor.y - pathPoint.anchor[1]) < 1) {
                        pointAlreadyDeclared = oldPointInfo.id;
                        break;
                    }
                }
                var pointInfo: P.IllustratorObject = null;
                if (pointAlreadyDeclared >= 0) {
                    pointInfo = container.getItem('marker', pointAlreadyDeclared);
                } else {
                    pointInfo = new P.IllustratorObject(pathPoint, 'marker');
                    pointInfo.belongsTo = itemInfo;
                    allPathPoints.push(pointInfo);
                    aruco.embedMarker(pointInfo.id, layerForMarker, pathPoint, 1000);
                    markerNum++;
                }

                if (k === 0) firstPointInfo = pointInfo;

                if ((k > 0 && k <= pathPoints.length) || (k === 1 && pathPoints.length === 2)) {
                    linkArray.push(new P.Link(previousPointInfo, pointInfo));
                }
                if (k === (pathPoints.length - 1) && pathItem.closed) {
                    linkArray.push(new P.Link(firstPointInfo, pointInfo));
                }
                previousPointInfo = pointInfo;
            }
        }
    }

    (<Application>document.parent).redraw();

    // output result
    let objects: Array<any> = new Array();
    container.listItem().forEach(function (element, index, array) {
        objects.push(element);
    });
    linkArray.forEach(function (element, index, array) {
        objects.push(element);
    })
    const objectsJson = JSON.stringify(objects, null, 2);

    const outputFileName = document.path.path + '/' + document.path.name + '/' + document.name.replace('.ai', '.json');
    const writeSucceeded = IO.writeToFile(outputFileName, objectsJson);
    if (writeSucceeded) {
        alert('結果を' + outputFileName + 'に出力しました');
    } else {
        alert('結果を' + outputFileName + 'に出力できませんでした');
    }
}

main(app.activeDocument);