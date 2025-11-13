import { useStore } from '../store'

export default function OutputPanel() {
  const { output } = useStore()

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
        Output
      </h2>
      <div className="bg-gray-900 text-green-400 font-mono text-sm p-4 rounded-lg h-64 overflow-y-auto">
        {output.length === 0 ? (
          <div className="text-gray-500">No output yet. Execute a command to see results.</div>
        ) : (
          output.map((line, index) => (
            <div key={index} className="mb-1">
              {line}
            </div>
          ))
        )}
      </div>
    </div>
  )
}

