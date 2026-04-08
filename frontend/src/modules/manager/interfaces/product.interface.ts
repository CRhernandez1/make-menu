export interface Category {
  id: number
  name: string
}

export interface Product {
  id: number
  name: string
  description: string
  price: number
  available: boolean
  product_image: string | null
  category: Category
}

export interface Ingredient {
  id: number
  name: string
  description: string
  ingredient_type: string
  available: boolean
}