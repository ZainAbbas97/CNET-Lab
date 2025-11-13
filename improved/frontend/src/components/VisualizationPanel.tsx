import { useMemo } from 'react'
import Plot from 'react-plotly.js'
import { useStore } from '../store'

export default function VisualizationPanel() {
  const { plotData } = useStore()

  const plotConfig = useMemo(() => {
    if (!plotData || plotData.format !== 'plotly') {
      return null
    }

    return {
      data: plotData.spec.data || [],
      layout: {
        ...plotData.spec.layout,
        autosize: true,
        responsive: true,
      },
      config: {
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d'],
        displaylogo: false,
      },
    }
  }, [plotData])

  if (!plotConfig) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
          Visualization
        </h2>
        <div className="flex items-center justify-center h-96 text-gray-500 dark:text-gray-400">
          No visualization yet. Generate a plot to see it here.
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
        Visualization
      </h2>
      <div className="bg-white rounded-lg p-4">
        <Plot
          data={plotConfig.data}
          layout={plotConfig.layout}
          config={plotConfig.config}
          style={{ width: '100%', height: '500px' }}
          useResizeHandler={true}
        />
      </div>
    </div>
  )
}

