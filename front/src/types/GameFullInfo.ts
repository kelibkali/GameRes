import type {Category, Price, ReleaseDate} from "./GameInList.ts";

export interface GameFullInfo {
    name:string;
    steam_appid:number,
    required_age?:number,
    is_free?:Boolean,
    description?:string,
    supported_languages?:string,
    header_image:string,
    developers?:Array<string>,
    publishers?:Array<string>,
    price_overview?:Price,
    release_date?:ReleaseDate,
    categories?:Array<Category>,
    genres?:Array<Category>,
    achievements?:any,
    has_chinese?:string,
    app_reviews?:Review,
    type?:string,
}

export interface Review{
    review_score_desc?:string,
    total_positive?:number,
    total_negative?:number,
    total_reviews?:number,
}
