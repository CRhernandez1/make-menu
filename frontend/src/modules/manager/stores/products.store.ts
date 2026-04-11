import { ref } from 'vue'
import { defineStore } from 'pinia'
import {
  getProductsAction,
  deleteProductAction,
  addProductAction,
  editProductAction,
  uploadProductImageAction,
  getCategoriesAction,
  getIngredientsAction,
  addIngredientAction,
  editIngredientAction,
  deleteIngredientAction,
  addCategoryAction,
  deleteCategoryAction,
  getAllergensAction,
} from '../actions/getProducts.action'
import type { Product, Category, Ingredient, Allergen } from '../interfaces/product.interface'

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

  const addProduct = async (cif: string, payload: object): Promise<number> => {
    const id = await addProductAction(cif, payload)
    await fetchProducts(cif)
    return id
  }

  const editProduct = async (cif: string, productId: number, payload: object) => {
    await editProductAction(cif, productId, payload)
    await fetchProducts(cif)
  }

  const deleteProduct = async (cif: string, productId: number) => {
    await deleteProductAction(cif, productId)
    products.value = products.value.filter(p => p.id !== productId)
  }

  const uploadProductImage = async (cif: string, productId: number, image: File) => {
    await uploadProductImageAction(cif, productId, image)
    await fetchProducts(cif)
  }

  // ── Categories ────────────────────────────────────────
  const categories = ref<Category[]>([])

  const fetchCategories = async (cif: string) => {
    categories.value = await getCategoriesAction(cif)
  }

  const addCategory = async (cif: string, name: string) => {
    await addCategoryAction(cif, name)
    await fetchCategories(cif)
  }

  const deleteCategory = async (cif: string, categoryId: number) => {
    await deleteCategoryAction(cif, categoryId)
    categories.value = categories.value.filter(c => c.id !== categoryId)
  }

  // ── Ingredients ───────────────────────────────────────
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

  // ── Allergens ─────────────────────────────────────────
  const allergens = ref<Allergen[]>([])

  const fetchAllergens = async () => {
    allergens.value = await getAllergensAction()
  }

  return {
    isLoading,
    products, fetchProducts, addProduct, editProduct, deleteProduct, uploadProductImage,
    categories, fetchCategories, addCategory, deleteCategory,
    ingredients, fetchIngredients, addIngredient, editIngredient, deleteIngredient,
    allergens, fetchAllergens,
  }
})