export function makeTable(data) {
  return (
    <table>
      <thead>
        <tr>
          <th>File Name</th>
          <th># of Commits</th>
        </tr>
      </thead>
      <tbody>
      {Object.keys(data).map(fileName =>
	<tr key={fileName}>
          <td>{fileName}</td>
	  <td style={{textAlign: 'center'}}>{data[fileName]}</td>
	</tr>
      )}
      </tbody>
    </table>
  )
}
