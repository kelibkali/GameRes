
declare module 'rellax'{
    export interface RellaxOptions{
        seppd?: number;
        horizontalSpeed?: number;
        xsSpeed?: number;
        xsHorizontalSpeed?: number;
        callback?: (positions: any) => void;
        breakpoints?: number[];
        relativeToWrapper?: boolean;
        round?: boolean;
        vertical?: 'vertical' | 'horizontal';
        wrapper?: string;
        selector?: string;
    }

    export interface RellaxInstance {
        refresh(): void;

        destroy(): void;

        positions: any[];
    }

    const Rellax: new (selector: string | Element | NodeListOf<Element>, options?: RellaxOptions) => RellaxInstance;

    export default Rellax;
}