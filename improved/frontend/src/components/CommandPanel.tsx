import { useState } from 'react'
import React from 'react'
import { useMutation } from '@tanstack/react-query'
import { executeCommand } from '../api/client'
import { useStore } from '../store'
import toast from 'react-hot-toast'

const ALLOWED_COMMANDS = ['plot', 'describe', 'corr', 'head', 'tail', 'info']

export default function CommandPanel() {
  const { sessionId, addOutput, dataset } = useStore()
  const [command, setCommand] = useState('plot')
  const [params, setParams] = useState({
    type: 'bar',
    x: '',
    y: '',
    title: '',
    xlabel: '',
    ylabel: '',
  })

  // Get available columns from dataset
  const availableColumns = dataset?.columns || []
  
  // Auto-select first two columns when dataset is loaded
  React.useEffect(() => {
    if (availableColumns.length > 0) {
      setParams(prev => ({
        ...prev,
        x: prev.x || availableColumns[0],
        y: prev.y || (availableColumns.length > 1 ? availableColumns[1] : '')
      }))
    }
  }, [dataset])

  const mutation = useMutation({
    mutationFn: () => {
      console.log('Executing command:', command, params, sessionId)
      return executeCommand(command, params, sessionId!)
    },
    onSuccess: (data) => {
      console.log('Command success response:', data)
      addOutput(`> ${command} ${JSON.stringify(params)}`)
      addOutput(JSON.stringify(data.result, null, 2))
      
      // Check if result has plotly format
      if (data.result && data.result.format === 'plotly') {
        console.log('Setting plot data:', data.result)
        useStore.getState().setPlotData(data.result)
        toast.success('Plot generated successfully')
      } else if (command === 'plot') {
        // If plot command but no plotly format, show error
        console.warn('Plot command but no plotly format:', data.result)
        toast.error('Failed to generate plot. Check output for details.')
      } else {
        toast.success('Command executed successfully')
      }
    },
    onError: (error: any) => {
      console.error('Command execution error:', error)
      
      // Handle FastAPI validation errors (422)
      let errorMsg = 'Command failed'
      if (error.response?.data) {
        const data = error.response.data
        if (Array.isArray(data.detail)) {
          // Pydantic validation errors
          errorMsg = data.detail.map((err: any) => 
            `${err.loc?.join('.') || ''}: ${err.msg || err}`
          ).join(', ')
        } else if (typeof data.detail === 'string') {
          errorMsg = data.detail
        } else if (data.detail) {
          errorMsg = JSON.stringify(data.detail)
        }
      } else if (error.message) {
        errorMsg = error.message
      }
      
      addOutput(`Error: ${errorMsg}`)
      toast.error(errorMsg)
    },
  })

  const handleExecute = () => {
    if (!sessionId) {
      toast.error('Please upload a dataset first')
      return
    }
    
    // Validate plot parameters
    if (command === 'plot') {
      if (params.type !== 'heatmap' && params.type !== 'histogram' && params.type !== 'pie') {
        if (!params.x || !params.y) {
          toast.error('Please select both X and Y axis columns')
          return
        }
      } else if (params.type === 'histogram' || params.type === 'pie') {
        if (!params.x) {
          toast.error('Please select X axis column')
          return
        }
      }
    }
    
    mutation.mutate()
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
        Command Panel
      </h2>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Command
          </label>
          <select
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          >
            {ALLOWED_COMMANDS.map((cmd) => (
              <option key={cmd} value={cmd}>
                {cmd}
              </option>
            ))}
          </select>
        </div>

        {command === 'plot' && (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Plot Type
              </label>
              <select
                value={params.type}
                onChange={(e) => setParams({ ...params, type: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="bar">Bar</option>
                <option value="line">Line</option>
                <option value="scatter">Scatter</option>
                <option value="histogram">Histogram</option>
                <option value="pie">Pie</option>
                <option value="heatmap">Heatmap</option>
                <option value="box">Box</option>
              </select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  X Axis
                </label>
                {availableColumns.length > 0 ? (
                  <select
                    value={params.x}
                    onChange={(e) => setParams({ ...params, x: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  >
                    <option value="">Select column...</option>
                    {availableColumns.map((col) => (
                      <option key={col} value={col}>
                        {col}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    type="text"
                    value={params.x}
                    onChange={(e) => setParams({ ...params, x: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    placeholder="Upload dataset first"
                    disabled
                  />
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Y Axis
                </label>
                {availableColumns.length > 0 ? (
                  <select
                    value={params.y}
                    onChange={(e) => setParams({ ...params, y: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  >
                    <option value="">Select column...</option>
                    {availableColumns.map((col) => (
                      <option key={col} value={col}>
                        {col}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    type="text"
                    value={params.y}
                    onChange={(e) => setParams({ ...params, y: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    placeholder="Upload dataset first"
                    disabled
                  />
                )}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Title (optional)
              </label>
              <input
                type="text"
                value={params.title}
                onChange={(e) => setParams({ ...params, title: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>
          </>
        )}

        <button
          onClick={handleExecute}
          disabled={!sessionId || mutation.isPending}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {mutation.isPending ? 'Executing...' : 'Execute Command'}
        </button>
      </div>
    </div>
  )
}



