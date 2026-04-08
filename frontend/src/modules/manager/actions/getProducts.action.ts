import { makeMenuApi } from '@/api/makeMenu'
import type { Product } from '../interfaces/product.interface'

export const getProductsAction = async (cif: string): Promise<Product[]> => {
  const { data } = await makeMenuApi.get(`/establishments/${cif}/products/`)
  return data
}

export const deleteProductAction = async (cif: string, productId: number): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/${productId}/delete/`)
}

export const addProductAction = async (cif: string, payload: object): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/add/`, payload)
}

export const editProductAction = async (cif: string, productId: number, payload: object): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/${productId}/edit/`, payload)
}

export const getCategoriesAction = async (cif: string): Promise<Category[]> => {
  const { data } = await makeMenuApi.get(`/establishments/${cif}/products/categories/`)
  return data
}

export const getIngredientsAction = async (cif: string): Promise<Ingredient[]> => {
  const { data } = await makeMenuApi.get(`/establishments/${cif}/products/ingredients/`)
  return data
}

export const addIngredientAction = async (cif: string, payload: object): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/ingredients/add/`, payload)
}

export const editIngredientAction = async (cif: string, ingredientId: number, payload: object): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/ingredients/${ingredientId}/edit`, payload)
}

export const deleteIngredientAction = async (cif: string, ingredientId: number): Promise<void> => {
  await makeMenuApi.post(`/establishments/${cif}/products/ingredients/${ingredientId}/delete`)
}