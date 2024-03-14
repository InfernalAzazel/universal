

export interface DocsConfigType {
  root: string
  locales: LocaleType[]
}

export interface LocaleType {
  mark: string
  label: string
  title: string
  indexLink: string
  sidebars: SidebarType[]
}

export interface SidebarType {
  id?: number
  title: string
  link?: string
  items?: SidebarType[]
}

