import { ref } from 'vue'
import { defineStore } from 'pinia'
import {
  getProductsAction,
  deleteProductAction,
  addProductAction,
  editProductAction,
} from '../actions/getProducts.action'
import type { Product } from '../interfaces/product.interface'

import { getCategoriesAction } from '../actions/getProducts.action'
import type { Category } from '../interfaces/product.interface'

export const useProductsStore = defineStore('products', () => {
  const products = ref<Product[]>([])
  const isLoading = ref(false)

  const fetchProducts = async (cif: string) => {
    isLoading.value = true
    try {
      products.value = await getProductsAction(cif)
    } finally {
      isLoading.value = false
    }
  }

  const deleteProduct = async (cif: string, productId: number) => {
    await deleteProductAction(cif, productId)
    products.value = products.value.filter(p => p.id !== productId)
  }

  const addProduct = async (cif: string, payload: FormData) => {
    await addProductAction(cif, payload)
    await fetchProducts(cif)
  }

  const editProduct = async (cif: string, productId: number, payload: FormData) => {
  await editProductAction(cif, productId, payload)
  await fetchProducts(cif)
}

    const categories = ref<Category[]>([])

    const fetchCategories = async (cif: string) => {
    categories.value = await getCategoriesAction(cif)
    }

    return { products, categories, isLoading, fetchProducts, fetchCategories, deleteProduct, addProduct, editProduct }
})


