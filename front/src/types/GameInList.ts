export interface GameInList {
    app_id:number,
    name:string,
    steam_appid?:number,
    required_age?:number,
    is_free?:Boolean,
    description?:string,
    supported_languages?:string,
    header_image?:string,
    developers?:Array<string>,
    publishers?:Array<string>,
    price_overview?:Price,
    release_date?:ReleaseDate,
    categories?:Array<Category>,
    genres?:Array<Category>,
    playtime_forever?:number,
    playtime_2weeks?:number,
    achieved_count?:number,
    achievements_total?:number,
}

export interface Price{
    currency:string,
    initial:number,
    final:number,
    discount_percent:number,
    initial_formatted:string,
    final_formatted:string,
}

export interface ReleaseDate{
    coming_soon:boolean,
    date:string,
}

export interface Category{
    id:string,
    description:string,
}

