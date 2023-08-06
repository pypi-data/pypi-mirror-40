const arucoMarkerPath: string = './aruco6x6_250/';

function arucoFileName(idx: number): string {
    if (idx < 0 || idx > 250) {
        throw new Error('250 markers are parepared, you may be exceeds the limit');
    }
    return 'aruco6x6_' + String(idx) + '.jpg';
}

function addLayerForArucoMarker(document: Document): Layer {
    const layer = document.layers.add();
    layer.name = 'marker';
    layer.zOrder(ZOrderMethod.BRINGTOFRONT);

    return layer;
}

function embedMarker(id: number, layer: Layer, point: PathPoint, size: number): void {
    var newMarker: PlacedItem = layer.placedItems.add();
    newMarker.file = new File(arucoMarkerPath + arucoFileName(id));
    let newPosition = point.anchor;
    newPosition[0] -= newMarker.width / 2;
    newPosition[1] += newMarker.height / 2;
    newMarker.position = newPosition;
    newMarker.resize(size / newMarker.width, size / newMarker.height);
    newMarker.embed();
}

export { arucoFileName, addLayerForArucoMarker, embedMarker };