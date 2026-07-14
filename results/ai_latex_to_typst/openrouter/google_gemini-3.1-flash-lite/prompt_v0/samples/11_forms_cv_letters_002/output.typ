#set page(paper: "a4", margin: (top: 1.27cm, left: 1cm, right: 1cm, bottom: 2cm))
#set text(font: "Helvetica", lang: "en")

#let ecvitem(label, content, spacing: 0pt) = {
  grid(
    columns: (30%, 70%),
    column-gutter: 1em,
    strong(label),
    content
  )
  v(spacing)
}

#let section(title) = {
  v(1em)
  text(size: 1.2em, weight: "bold", title)
  line(length: 100%, stroke: 0.5pt)
  v(0.5em)
}

#let SignatureAndDate(name) = {
  v(2em)
  grid(
    columns: (1fr, 1fr),
    column-gutter: 2em,
    [Place (Province), #datetime.today().display("[day] [month repr:long] [year]")], [],
    line(length: 100%), line(length: 100%),
    [Place and date], name
  )
}

#align(center, text(size: 1.5em, weight: "bold")[Name, Surname])

#v(1em)

#grid(
  columns: (1fr, 1fr),
  [
    Address: (Remove if not relevant) \
    Telephone: (Remove if not relevant) \
    Fax: (Remove if not relevant) \
    E-mail: #link("mailto:email@email.com")[email\@email.com] \
  ],
  [
    Professional: #link("mailto:email@email.it")[email\@email.it] \
    PEC: #link("mailto:emailo@pec.it")[email\@pec.it] \
    Homepage: #link("http://www.homepage.com")[www.homepage.com] \
    YouTube: #link("http://www.youtube.com/myChannel")[www.youtube.com/myChannel] \
  ]
)

#v(1em)

#ecvitem(text(size: 1.1em)[Desired employment / Occupational field], text(size: 1.1em)[(Remove if not relevant)])

#section("Work experience")
#ecvitem("Dates", [Add separate entries for each relevant post occupied, starting from the most recent. (Remove if not relevant).])
#ecvitem("Occupation or position held", […])
#ecvitem("Main activities and responsibilities", […])
#ecvitem("Name and address of employer", […])
#ecvitem("Type of business or sector", […])

#section("Education and training")
#ecvitem("Dates", [Add separate entries for each relevant course you have completed, starting from the most recent. (Remove if not relevant).])
#ecvitem("Title of qualification awarded", […])
#ecvitem("Principal subjects/Occupational skills covered", […])
#ecvitem("Name and type of organization providing education and training", […])
#ecvitem("Level in national or international classification", […])

#section("Personal skills and competences")
#ecvitem("Mother tongue", [Specify mother tongue], spacing: 5pt)
#ecvitem(text(size: 1.1em)[Other language(s)], [])
#table(columns: (1fr, 1fr, 1fr, 1fr, 1fr), stroke: none,
  table.header([Language], [Listening], [Reading], [Spoken interaction], [Spoken production]),
  [Language], [], [], [], [],
  [Language], [], [], [], []
)

#ecvitem(text(size: 1.1em)[Social skills and competences], [Replace this text by a description of these competences and indicate where they were acquired (remove if not relevant).], spacing: 10pt)
#ecvitem(text(size: 1.1em)[Organisational skills and competences], [Replace this text by a description of these competences and indicate where they were acquired (remove if not relevant).], spacing: 10pt)
#ecvitem(text(size: 1.1em)[Technical skills and competences], [Replace this text by a description of these competences and indicate where they were acquired (remove if not relevant).], spacing: 10pt)
#ecvitem(text(size: 1.1em)[Computer skills and competences], [Replace this text by a description of these competences and indicate where they were acquired (remove if not relevant).], spacing: 10pt)
#ecvitem(text(size: 1.1em)[Artistic skills and competences], [Replace this text by a description of these competences and indicate where they were acquired (remove if not relevant).], spacing: 10pt)
#ecvitem(text(size: 1.1em)[Other skills and competences], [Replace this text by a description of these competences and indicate where they were acquired (remove if not relevant).], spacing: 10pt)
#ecvitem(text(size: 1.1em)[Driving licence(s)], [State here whether you hold a driving licence and if so for which categories of vehicle. (Remove if not relevant).])

#section("Additional information")
#ecvitem("", [Include here any other information that may be relevant, for example contact persons, references, etc. (Remove heading if not relevant).], spacing: 10pt)
#ecvitem("", strong("Personal interests"))
#ecvitem("", […])

#section("Annexes")
#ecvitem("", [List any item attached to the CV])

#v(5cm)
#SignatureAndDate([Name Surname])
