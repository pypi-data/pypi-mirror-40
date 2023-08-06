import os
import boto3

from dealstat.dealstat import compress_dir

class Boto:

    def __init__(self, service, aws_access_key_id=None, aws_secret_access_key=None):

        self.service = service

        if not aws_access_key_id or aws_secret_access_key:
            aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
            aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

        self.client = boto3.client(service, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.resource = boto3.resource(service, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


    def get_temp_url(self, location):
        return self.client.generate_presigned_url(ClientMethod = 'get_object', Params = {'Bucket':location['bucket'], 'Key':location['key']})


    def move_object(self, old_location, new_location, delete_original=False):
        self.resource.Object(new_location['bucket'], new_location['key']).copy_from(CopySource='{}/{}'.format(old_location['bucket'], old_location['key']))

        if delete_original:
            self.resource.Object(Bucket=old_location['bucket'], Key=old_location['key']).delete()


    def upload_file(self, file_path, location):
        return self.resource.Bucket(location['bucket']).upload_file(file_path, location['key'])


    def download_file(self, file_path, location):
        return self.resource.Bucket(location['bucket']).download_file(location['key'], file_path)


    def compress_and_upload(self, dir_path, location):
        compressed_file = compress_dir(dir_path)
        self.upload_file(compressed_file, location)
        os.remove(compressed_file)


    def list_bucket(self, bucket, prefix=None, exclude_dirs=True):
        bucket = self.resource.Bucket(bucket)

        if prefix:
            initial_result = bucket.objects.filter(Prefix=prefix)
        else:
            initial_result = bucket.objects.all()

            
        if exclude_dirs:
            final_result = [i for i in initial_result if not i.key.endswith('/')]
        else:
            final_result = initial_result

        return final_result

if __name__ == '__main__':
    s3 = Boto('s3')
    s3.zip_and_upload('/Users/ecatkins/Downloads/Sample_Deeds', {'bucket':'dealstat-public-misc', 'key':'lol.tar.gz'})
