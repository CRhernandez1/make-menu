const dateFormatter = new Intl.DateTimeFormat('es-ES', {
  day: '2-digit',
  month: '2-digit',
  hour: '2-digit',
  minute: '2-digit',
})

const timeFormatter = new Intl.DateTimeFormat('es-ES', {
  hour: '2-digit',
  minute: '2-digit',
})

export function useFormatters() {
  const formatDate = (dateString: string): string => {
    if (!dateString) return ''
    return dateFormatter.format(new Date(dateString))
  }

  const formatTime = (iso: string): string => {
    return timeFormatter.format(new Date(iso))
  }

  const elapsedTime = (iso: string): string => {
    const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 60000)
    if (diff < 1) return 'ahora'
    if (diff < 60) return `${diff} min`
    return `${Math.floor(diff / 60)}h ${diff % 60}m`
  }

  const isUrgent = (placedAt: string, thresholdMinutes = 15): boolean => {
    return Math.floor((Date.now() - new Date(placedAt).getTime()) / 60000) >= thresholdMinutes
  }

  return { formatDate, formatTime, elapsedTime, isUrgent }
}
