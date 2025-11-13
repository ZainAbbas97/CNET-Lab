import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { useMutation } from '@tanstack/react-query'
import { uploadDataset } from '../api/client'
import { useStore } from '../store'
import toast from 'react-hot-toast'

export default function FileUpload() {
  const { setSessionId, setDataset } = useStore()

  const mutation = useMutation({
    mutationFn: uploadDataset,
    onSuccess: (data) => {
      setSessionId(data.session_id)
      setDataset(data.dataset)
      toast.success(`Dataset loaded: ${data.dataset.rows} rows, ${data.dataset.columns.length} columns`)
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to upload dataset')
    },
  })

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      mutation.mutate(acceptedFiles[0])
    }
  }, [mutation])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
    },
    maxFiles: 1,
  })

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
        Upload Dataset
      </h2>
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
            : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
        } ${mutation.isPending ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <input {...getInputProps()} disabled={mutation.isPending} />
        {mutation.isPending ? (
          <div className="text-gray-600 dark:text-gray-400">Uploading...</div>
        ) : isDragActive ? (
          <div className="text-blue-600 dark:text-blue-400">Drop the CSV file here</div>
        ) : (
          <div>
            <p className="text-gray-600 dark:text-gray-400 mb-2">
              Drag & drop a CSV file here, or click to select
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-500">
              CSV files only, max 100MB
            </p>
          </div>
        )}
      </div>
      {mutation.isError && (
        <p className="mt-2 text-sm text-red-600 dark:text-red-400">
          {mutation.error?.response?.data?.detail || 'Upload failed'}
        </p>
      )}
    </div>
  )
}

