import { makeMenuApi } from '@/api/makeMenu'
import type { Product, Category, Ingredient, Allergen } from '../interfaces/product.interface'

// Products
export const getProductsAction = async (cif: string): Promise<Product[]> => {
  const { data } = await makeMenuApi.get(`/establishments/${cif}/products/`)
  return data
}

export const addProductAction = async (cif: string, payload: object): Promise<number> => {
  const { data } = await makeMenuApi.post(`/establishments/${cif}/products/add/`, payload)
  return data.id
}

export const editProductAction = async (cif: string, productId: number, payload: object): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/${productId}/edit/`, payload)
}

export const deleteProductAction = async (cif: string, productId: number): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/${productId}/delete/`)
}

export const uploadProductImageAction = async (cif: string, productId: number, image: File): Promise<void> => {
  const formData = new FormData()
  formData.append('product_image', image)
  await makeMenuApi.post(`/establishments/${cif}/products/${productId}/image/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

// Categories
export const getCategoriesAction = async (cif: string): Promise<Category[]> => {
  const { data } = await makeMenuApi.get(`/establishments/${cif}/products/categories/`)
  return data
}

export const addCategoryAction = async (cif: string, name: string): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/categories/add/`, { name })
}

export const deleteCategoryAction = async (cif: string, categoryId: number): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/categories/${categoryId}/delete/`)
}

// Ingredients
export const getIngredientsAction = async (cif: string): Promise<Ingredient[]> => {
  const { data } = await makeMenuApi.get(`/establishments/${cif}/products/ingredients/`)
  return data
}

export const addIngredientAction = async (cif: string, payload: object): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/ingredients/add/`, payload)
}

export const editIngredientAction = async (cif: string, ingredientId: number, payload: object): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/ingredients/${ingredientId}/edit/`, payload)
}

export const deleteIngredientAction = async (cif: string, ingredientId: number): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/ingredients/${ingredientId}/delete/`)
}

// Allergens
export const getAllergensAction = async (): Promise<Allergen[]> => {
  const { data } = await makeMenuApi.get('/allergens/')
  return data
}