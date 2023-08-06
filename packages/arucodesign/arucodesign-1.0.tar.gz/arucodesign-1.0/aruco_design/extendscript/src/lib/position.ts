/*点・図形の相対的な位置関係についてのロジック */

// 点の絶対座標
class Coordinate {
    constructor(
        public x: number,
        public y: number
    ) { }
}

// Itemの絶対座標
class AbsolutePosition {
    constructor(
        public anchor: Coordinate,
        public width: number,
        public height: number
    ) { }

    static fromPageItem(item: PageItem): AbsolutePosition {
        let anchor = {
            x: item.position[0],
            y: item.position[1]
        };
        return new AbsolutePosition(anchor, item.width, item.height);
    }

    static fromPathPoint(item: PathPoint): AbsolutePosition {
        let anchor = {
            x: item.anchor[0],
            y: item.anchor[1]
        }
        return new AbsolutePosition(anchor, 0, 0);
    }

    getCenterCoordinate(): Coordinate {
        const x = this.anchor.x + this.width / 2;
        const y = this.anchor.y - this.height / 2;

        return new Coordinate(x, y);
    }

    relativeTo(position: AbsolutePosition): RelativePosition {
        return calculateRelativePosition(position, this);
    }
}

// Item同士の相対座標
class RelativePosition {
    constructor(
        public x: number, // anchor同士の距離
        public y: number, // anchor同士の距離
        public distance: number // Itemの外縁部同士の最短距離
    ) { }

}

// オブジェクトのID
class IllustratorObject {
    public object: PageItem | PathPoint;
    public objectType: string;
    public id: number;
    public position: AbsolutePosition;
    public belongsTo?: IllustratorObject;
    public relativePosition?: RelativePosition;

    relativeTo(item: IllustratorObject): RelativePosition {
        return this.position.relativeTo(item.position);
    }

    setBelongsTo(item: IllustratorObject, relativePosition?: RelativePosition): void {
        this.belongsTo = item;
        this.relativePosition = relativePosition || this.relativeTo(item);
    }

    constructor(item: PageItem | PathPoint, objectType?: string, register: boolean = true) {
        this.object = item;
        this.objectType = objectType || 'unknown';
        //this.position = new AbsolutePosition(new Coordinate(0, 0), 0, 0);
        if (item.typename.indexOf("Item") !== -1) {
            this.position = AbsolutePosition.fromPageItem(<PageItem>item);
        } else {
            this.position = AbsolutePosition.fromPathPoint(<PathPoint>item);
        }

        this.belongsTo = null;
        this.relativePosition = null;

        if (register) {
            const container = IllustratorObjectContainer.getInstance();
            this.id = container.registerItem(this);
        }
    }

    toJSON(): any {
        return {
            objectType: this.objectType,
            id: this.id,
            belongsTo: this.belongsTo ? this.belongsTo.id : null
        };
    }
}

class Link {

    public objectType: string;
    public p1: IllustratorObject;
    public p2: IllustratorObject;

    constructor(
        p1: IllustratorObject,
        p2: IllustratorObject
    ) {
        this.objectType = 'link';
        this.p1 = p1;
        this.p2 = p2;
    }

    toJSON(): any {
        return {
            objectType: "link",
            p1: this.p1.id,
            p2: this.p2.id
        };
    }
}

class IllustratorObjectContainer {
    private static _instance: IllustratorObjectContainer;

    private _container: { [key: string]: Array<IllustratorObject>; }

    registerItem(object: IllustratorObject): number {
        const objectType = object.objectType;
        let num: number;
        if (!this._container[objectType]) {
            this._container[objectType] = new Array(object);
            num = 0;
        } else {
            num = this._container[objectType].push(object) - 1;
        }

        return num;
    }

    getItem(type: string, id: number): IllustratorObject {
        return this._container[type][id];
    }

    listItem(): Array<IllustratorObject> {
        let arr: Array<IllustratorObject> = new Array();
        for (var groupName in this._container) {
            arr = arr.concat(this._container[groupName]);
        }

        return arr;
    }

    public static getInstance(): IllustratorObjectContainer {
        if (!this._instance) {
            this._instance = new IllustratorObjectContainer(IllustratorObjectContainer.getInstance);
        }

        return this._instance
    }

    constructor(caller: Function) {
        if (caller !== IllustratorObjectContainer.getInstance) {
            throw new Error('Invalid initialization');
        } else if (IllustratorObjectContainer._instance) {
            throw new Error('IllustratorObjectContainer already initialized');
        }

        this._container = {};
    }
}

function calculateRelativePosition(position1, position2: AbsolutePosition): RelativePosition {
    let center1 = position1.getCenterCoordinate();
    let center2 = position2.getCenterCoordinate();

    let x = center2.x - center1.x;
    let y = center2.y - center1.y;

    let isXOverWrapped = Math.abs(x) < (Math.abs(position1.width) + Math.abs(position2.width)) / 2;
    let isYOverWrapped = Math.abs(y) < (Math.abs(position1.height) + Math.abs(position2.height)) / 2;

    let distance: number;
    if (isXOverWrapped && isYOverWrapped) distance = 0;
    else if (isXOverWrapped && !isYOverWrapped) distance = Math.abs(y) - (Math.abs(position1.height) + Math.abs(position2.height)) / 2;
    else if (!isXOverWrapped && isYOverWrapped) distance = Math.abs(x) - (Math.abs(position1.width) + Math.abs(position2.width)) / 2;
    else {
        let closestX = center1.x > center2.x ? position1.anchor.x - position2.anchor.x - position2.width : position2.anchor.x - position1.anchor.x - position1.width;
        let closestY = center1.y > center2.y ? position1.anchor.y - position2.anchor.y - position2.height : position2.anchor.y - position1.anchor.y - position1.height;
        distance = Math.sqrt(Math.pow(closestX, 2) + Math.pow(closestY, 2));
    }

    return new RelativePosition(x, y, distance);

}

export { Coordinate, AbsolutePosition, RelativePosition, IllustratorObject, IllustratorObjectContainer, Link };