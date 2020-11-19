node {
  properties(
    [
        parameters(
            [password(name: 'AWS_ACCESS_KEY_ID'),
             password(name: 'AWS_SECRET_ACCESS_KEY')]
            )

    ])
    stage('Checkout Github Repo') {
      checkout scm
    }

    stage('Deploy Cloudformation Stack') {
      sh 'python3 cloudformation_factory.py'
    }
}
