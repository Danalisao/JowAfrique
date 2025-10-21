'use client'

import { ShoppingCart, Plus } from 'lucide-react'

export default function CartPage() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6 flex items-center">
        <ShoppingCart className="mr-2 text-primary-500" size={24} />
        Panier
      </h1>
      
      <div className="text-center py-12">
        <ShoppingCart className="mx-auto text-gray-400 mb-4" size={64} />
        <h2 className="text-xl font-semibold mb-2">Votre panier est vide</h2>
        <p className="text-gray-400 mb-6">Ajoutez des ingrédients à votre liste de courses</p>
        <button className="px-6 py-3 bg-primary-500 text-white rounded-lg flex items-center mx-auto">
          <Plus className="mr-2" size={20} />
          Créer une liste
        </button>
      </div>
    </div>
  )
}
