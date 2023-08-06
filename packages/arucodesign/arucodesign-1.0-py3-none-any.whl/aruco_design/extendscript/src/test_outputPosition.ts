import 'extendscript-es5-shim-ts';
import * as P from './lib/position';
import * as IO from './lib/io';


function main(document: Document): void {
    /* `object`用のpathと`object`に付ける蛍光`marker`のポジションを出力する

    `object`の情報は`object`というレイヤに、マーカの情報は`marker`というレイヤに入っていると仮定する
    */

    const layers = document.layers;
    let objects: Array<P.IllustratorObject> = new Array();
    let markers: Array<P.IllustratorObject> = new Array();

    for (var i: number = 0; i < layers.length; i++) {

        var layer: Layer = layers[i];
        switch (layer.name) {
            case "object":
                for (var j: number = 0; j < layer.pathItems.length; j++) {
                    let item: PathItem = layer.pathItems[j];
                    let object = new P.IllustratorObject(item, 'object');
                    objects.push(object);
                }
            case "marker":
                for (var j: number = 0; j < layer.rasterItems.length; j++) {
                    let item: RasterItem = layer.rasterItems[j];
                    let marker = new P.IllustratorObject(item, 'marker');
                    markers.push(marker);
                }
            default:
                continue;
        }
    }

    if (objects.length == 0 || markers.length == 0) {
        const emptyLayerName: string = objects.length == 0 ? "`object`" : "`marker`";
        alert("No artwork found on" + emptyLayerName);
        return;
    }

    // `object`・マーカをそれぞれ求める。各`object`と`marker`の組み合わせについてそれぞれどこについているかを出力する
    for (var i: number = 0; i < markers.length; i++) {
        let marker = markers[i];
        let minDistance = Infinity;
        let distances: number[] = new Array();
        for (var j: number = 0; j < objects.length; j++) {
            let object = objects[j];
            let positionDiff = marker.relativeTo(object)
            if (minDistance > positionDiff.distance) {
                minDistance = positionDiff.distance;
                marker.setBelongsTo(object, positionDiff);
            }
        }
    }

    let alertString = "Result\n";

    alertString += 'Object:\n';
    alertString += JSON.stringify(objects, null, 2) + '\n';
    alertString += '\n\nMarker:\n';
    alertString += JSON.stringify(markers, null, 2) + '\n';
    alert(alertString);
    const outputFileName = document.path.path + '/' + document.path.name + '/' + document.name.replace('.ai', '.json');
    const writeSucceeded = IO.writeToFile(outputFileName, JSON.stringify(objects.concat(markers), null, 2));
    if (writeSucceeded) {
        alert('結果を' + outputFileName + 'に出力しました');
    } else {
        alert('結果を' + outputFileName + 'に出力できませんでした');
    }
}

export { main };

main(app.activeDocument);