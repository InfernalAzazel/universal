

export interface DocsConfigType {
  title: string
  root: string
  locales: LocaleType[]
}

export interface LocaleType {
  mark: string
  label: string
  indexLink: string
  sidebars: SidebarType[]
}

export interface SidebarType {
  id?: number
  title: string
  link?: string
  items?: SidebarType[]
}

