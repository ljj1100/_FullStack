def save_to_file(file_name, jobs):
  file = open(f"./{file_name}.csv", "w", encoding="utf-8-sig")
  file.write("Title, Company, Location, URL, NOTE\n")

  for job in jobs:
      file.write(
          f"{job['title']}, {job['company']},{job['location']},{job['link']},{job['note']}\n"
  )

  file.close()
