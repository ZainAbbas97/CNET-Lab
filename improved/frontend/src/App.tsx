import { useState } from 'react'
import FileUpload from './components/FileUpload'
import CommandPanel from './components/CommandPanel'
import OutputPanel from './components/OutputPanel'
import VisualizationPanel from './components/VisualizationPanel'
import { useStore } from './store'

function App() {
  const { sessionId, dataset } = useStore()

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Python Data Visualization System
          </h1>
          {sessionId && (
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Session: {sessionId.substring(0, 8)}... | 
              {dataset && ` Dataset: ${dataset.rows} rows, ${dataset.columns.length} columns`}
            </p>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column */}
          <div className="space-y-6">
            <FileUpload />
            <CommandPanel />
            <OutputPanel />
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            <VisualizationPanel />
          </div>
        </div>
      </main>
    </div>
  )
}

export default App

