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