export function makeTable(data) {
  return (
    <>
      <table style={ { marginTop: "60px" } }>
        <thead>
          <tr>
            <th>File Name</th>
            <th># of Fixes</th>
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
        <p style={ {width: "600px", fontSize: "16px", marginLeft: "20px"} }>
          <b>Each row of the table details</b>
      <br/>&nbsp;<code style={ { margin: "5px 0", fontSize: "15px"} }>number of fixes per file</code><br/>
          where <i>fixes</i> are commit messages containing keywords such as 'bug', 'fix', or 'issue'.
        </p>
    </>
  )
}
