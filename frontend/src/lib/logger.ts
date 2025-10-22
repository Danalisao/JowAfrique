/**
 * Logger centralisé pour l'application
 * Remplace console.log/error par un système plus robuste
 */

export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3
}

class Logger {
  private level: LogLevel = LogLevel.INFO

  setLevel(level: LogLevel) {
    this.level = level
  }

  private shouldLog(level: LogLevel): boolean {
    return level >= this.level
  }

  private formatMessage(level: string, message: string, ...args: any[]): string {
    const timestamp = new Date().toISOString()
    return `[${timestamp}] [${level}] ${message}`
  }

  debug(message: string, ...args: any[]) {
    if (this.shouldLog(LogLevel.DEBUG)) {
      console.debug(this.formatMessage('DEBUG', message), ...args)
    }
  }

  info(message: string, ...args: any[]) {
    if (this.shouldLog(LogLevel.INFO)) {
      console.info(this.formatMessage('INFO', message), ...args)
    }
  }

  warn(message: string, ...args: any[]) {
    if (this.shouldLog(LogLevel.WARN)) {
      console.warn(this.formatMessage('WARN', message), ...args)
    }
  }

  error(message: string, error?: Error, ...args: any[]) {
    if (this.shouldLog(LogLevel.ERROR)) {
      console.error(this.formatMessage('ERROR', message), error, ...args)
    }
  }

  // Méthodes spécialisées pour l'API
  apiError(endpoint: string, error: any) {
    this.error(`API Error [${endpoint}]`, error)
  }

  apiSuccess(endpoint: string, data?: any) {
    this.info(`API Success [${endpoint}]`, data)
  }

  // Méthodes spécialisées pour les composants
  componentError(component: string, action: string, error: any) {
    this.error(`Component Error [${component}.${action}]`, error)
  }

  componentAction(component: string, action: string, data?: any) {
    this.debug(`Component Action [${component}.${action}]`, data)
  }
}

// Instance singleton
export const logger = new Logger()

// Configuration par défaut
if (process.env.NODE_ENV === 'development') {
  logger.setLevel(LogLevel.DEBUG)
} else {
  logger.setLevel(LogLevel.WARN)
}

export default logger
