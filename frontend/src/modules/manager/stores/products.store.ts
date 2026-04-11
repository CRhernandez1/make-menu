import { ref } from 'vue'
import { defineStore } from 'pinia'
import {
  getProductsAction,
  deleteProductAction,
  addProductAction,
  editProductAction,
  getCategoriesAction,
  getIngredientsAction,
  addIngredientAction,
  editIngredientAction,
  deleteIngredientAction,
} from '../actions/getProducts.action'
import type { Product, Category, Ingredient } from '../interfaces/product.interface'

export const useProductsStore = defineStore('products', () => {
  const isLoading = ref(false)

  // ── Products ──────────────────────────────────────────
  const products = ref<Product[]>([])

  const fetchProducts = async (cif: string) => {
    isLoading.value = true
    try {
      products.value = await getProductsAction(cif)
    } finally {
      isLoading.value = false
    }
  }

  const addProduct = async (cif: string, payload: FormData) => {
    await addProductAction(cif, payload)
    await fetchProducts(cif)
  }

  const editProduct = async (cif: string, productId: number, payload: FormData) => {
    await editProductAction(cif, productId, payload)
    await fetchProducts(cif)
  }

  const deleteProduct = async (cif: string, productId: number) => {
    await deleteProductAction(cif, productId)
    products.value = products.value.filter(p => p.id !== productId)
  }

  // Categories 
  const categories = ref<Category[]>([])

  const fetchCategories = async (cif: string) => {
    categories.value = await getCategoriesAction(cif)
  }

  // Ingredients 
  const ingredients = ref<Ingredient[]>([])

  const fetchIngredients = async (cif: string) => {
    isLoading.value = true
    try {
      ingredients.value = await getIngredientsAction(cif)
    } finally {
      isLoading.value = false
    }
  }

  const addIngredient = async (cif: string, payload: object) => {
    await addIngredientAction(cif, payload)
    await fetchIngredients(cif)
  }

  const editIngredient = async (cif: string, ingredientId: number, payload: object) => {
    await editIngredientAction(cif, ingredientId, payload)
    await fetchIngredients(cif)
  }

  const deleteIngredient = async (cif: string, ingredientId: number) => {
    await deleteIngredientAction(cif, ingredientId)
    ingredients.value = ingredients.value.filter(i => i.id !== ingredientId)
  }

  return {
    isLoading,
    products, fetchProducts, addProduct, editProduct, deleteProduct,
    categories, fetchCategories,
    ingredients, fetchIngredients, addIngredient, editIngredient, deleteIngredient,
  }
})