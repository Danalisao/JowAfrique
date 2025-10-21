'use client'

export default function StatusBar() {
  return (
    <div className="status-bar">
      <div className="text-white font-medium">09:41</div>
      <div className="flex items-center space-x-1">
        <div className="w-4 h-3 border border-white rounded-sm">
          <div className="w-3 h-2 bg-white rounded-sm m-0.5"></div>
        </div>
        <div className="w-4 h-3 border border-white rounded-sm">
          <div className="w-3 h-2 bg-white rounded-sm m-0.5"></div>
        </div>
        <div className="w-6 h-3 border border-white rounded-sm">
          <div className="w-5 h-2 bg-white rounded-sm m-0.5"></div>
        </div>
      </div>
    </div>
  )
}
