import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { executeCommand } from '../api/client'
import { useStore } from '../store'
import toast from 'react-hot-toast'

const ALLOWED_COMMANDS = ['plot', 'describe', 'corr', 'head', 'tail', 'info']

export default function CommandPanel() {
  const { sessionId, addOutput } = useStore()
  const [command, setCommand] = useState('plot')
  const [params, setParams] = useState({
    type: 'bar',
    x: 'rooms',
    y: 'price',
    title: '',
    xlabel: '',
    ylabel: '',
  })

  const mutation = useMutation({
    mutationFn: () => executeCommand(command, params, sessionId!),
    onSuccess: (data) => {
      addOutput(`> ${command} ${JSON.stringify(params)}`)
      addOutput(JSON.stringify(data.result, null, 2))
      if (data.result.format === 'plotly') {
        useStore.getState().setPlotData(data.result)
      }
      toast.success('Command executed successfully')
    },
    onError: (error: any) => {
      addOutput(`Error: ${error.response?.data?.detail || 'Command failed'}`)
      toast.error(error.response?.data?.detail || 'Command failed')
    },
  })

  const handleExecute = () => {
    if (!sessionId) {
      toast.error('Please upload a dataset first')
      return
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
                <input
                  type="text"
                  value={params.x}
                  onChange={(e) => setParams({ ...params, x: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  placeholder="Column name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Y Axis
                </label>
                <input
                  type="text"
                  value={params.y}
                  onChange={(e) => setParams({ ...params, y: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  placeholder="Column name"
                />
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

